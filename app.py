from flask import Flask, render_template, request, redirect, session, jsonify, url_for, send_file
import mysql.connector
from enkrip import encrypt as aes_encrypt, decrypt as aes_decrypt, get_mode
import base64
import bcrypt
from datetime import datetime
from reportlab.pdfgen import canvas
import os
import io
import qrcode
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.units import cm
import random
import string
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from collections import OrderedDict
import calendar

app = Flask(__name__) # type: ignore
app.secret_key = 'supersecretkey'

key = b'16byteslongkey!!'
mode = get_mode("CBC") 

def encrypt(text):
    ciphertext_b64, iv = aes_encrypt(text, key, mode)
    if iv:
        iv_b64 = base64.b64encode(iv).decode()
        return f"{iv_b64}::{ciphertext_b64}"
    return ciphertext_b64

def decrypt(token):
    if "::" in token:
        iv_b64, ciphertext_b64 = token.split("::")
        iv = base64.b64decode(iv_b64)
        return aes_decrypt(ciphertext_b64, key, mode)
    else:
        return aes_decrypt(token, key, mode)

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='villashield'
    )

# 🔹 Dashboard route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass'].encode()

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur.execute("INSERT INTO users (name, email, pass) VALUES (%s, %s, %s)",
                    (name, email, hashed_password.decode()))
        db.commit()
        cur.close()
        db.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor(dictionary=True)
        email_input = request.form['email']
        password_input = request.form['pass'].encode()
        
        cur.execute("SELECT * FROM users WHERE email=%s", (email_input,))
        user = cur.fetchone()
        
        cur.close()
        db.close()

        if user and bcrypt.checkpw(password_input, user['pass'].encode()):
            session['user_id'] = user['id']
            session['user_name'] = user['NAME']
            session['user_email'] = user['email']
            session['role'] = user.get('role', 'user')  # default 'user' jika kolom role belum ada
            
            if session['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else:
            return render_template('login.html', error="Email atau password salah")
    
    return render_template('login.html')



@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin.html')

@app.route('/admin/bookings', methods=['GET', 'POST'])
def admin_bookings():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Ambil parameter filter
    kode_booking = request.args.get('kode_booking')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    tipe_villa = request.args.get('tipe_villa')

    query = """
        SELECT b.*, u.name 
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        WHERE 1=1
    """
    params = []

    if kode_booking:
        query += " AND b.kode_booking LIKE %s"
        params.append(f"%{kode_booking}%")
    if checkin:
        query += " AND b.checkin >= %s"
        params.append(checkin)
    if checkout:
        query += " AND b.checkout <= %s"
        params.append(checkout)
    if tipe_villa:
        query += " AND b.tipe_villa = %s"
        params.append(tipe_villa)

    query += " ORDER BY b.checkin DESC"
    cur.execute(query, tuple(params))
    data = cur.fetchall()
    cur.close()
    db.close()

    decrypted_data = []
    for d in data:
        try:
            identitas_asli = decrypt(d['identitas'])
        except:
            identitas_asli = "[Gagal didekripsi]"
        decrypted_data.append({
            'id': d['id'],
            'nama_user': d['name'] if d['user_id'] else 'Admin',
            'nama': d['nama'],
            'identitas': identitas_asli,
            'tipe_villa': d['tipe_villa'],
            'no_villa': d['no_villa'],
            'checkin': d['checkin'].strftime("%Y-%m-%d"),
            'checkout': d['checkout'].strftime("%Y-%m-%d"),
            'total_harga': "Rp {:,}".format(d['total_harga']).replace(",", "."),
            'status_checkout': d['status_checkout']
        })

    return render_template('admin_bookings.html', bookings=decrypted_data)


@app.route('/admin/update_checkout/<int:booking_id>', methods=['POST'])
def update_checkout_status(booking_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE bookings SET status_checkout = %s WHERE id = %s", ('Sudah Checkout', booking_id))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/bookings/add', methods=['POST'])
def tambah_pesanan_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    nama = request.form.get('nama')
    identitas = request.form.get('identitas')
    kamar_raw = request.form.get('kamar')  # "Royal Sunset Villa - 2500000"

    if " - " not in kamar_raw:
        return "Format tipe villa salah.", 400

    tipe_villa, harga_str = kamar_raw.split(" - ")
    harga_per_malam = int(harga_str)

    no_villa = int(request.form.get('no_villa'))
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')

    t_checkin = datetime.strptime(checkin, "%Y-%m-%d")
    t_checkout = datetime.strptime(checkout, "%Y-%m-%d")
    lama_inap = (t_checkout - t_checkin).days
    if lama_inap <= 0:
        return "Tanggal checkout harus setelah checkin.", 400

    total_harga = harga_per_malam * lama_inap

    user_id = 15  # guest

    identitas_encrypted = encrypt(identitas)
    kode_booking = generate_kode_booking()

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO bookings (user_id, nama, identitas, tipe_villa, harga_per_malam, no_villa, checkin, checkout, lama_inap, total_harga, status_checkout, kode_booking)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, nama, identitas_encrypted, tipe_villa, harga_per_malam, no_villa,
          checkin, checkout, lama_inap, total_harga, 'Belum Checkout', kode_booking))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin_bookings'))



@app.route('/admin/bookings/form')
def form_pesanan_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('form_pesanan_admin.html')


@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT name, email, role FROM users WHERE is_deleted = FALSE")

    users = cur.fetchall()
    cur.close()
    db.close()

    return render_template('admin_users.html', users=users)

@app.route('/admin/users/delete', methods=['POST'])
def hapus_user():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    email = request.form.get('email')

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET is_deleted = TRUE WHERE email = %s", (email,))
    db.commit()
    cur.close()
    db.close()

    return redirect('/admin/users')


@app.route('/admin/stats')
def admin_statistik():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    bulan_param = request.args.get('bulan')
    db = get_db()
    cur = db.cursor()

    if bulan_param and bulan_param.isdigit():
        bulan = int(bulan_param)
        cur.execute("SELECT COUNT(*), SUM(total_harga) FROM bookings WHERE MONTH(checkin) = %s", (bulan,))
        count, total = cur.fetchone()
    else:
        bulan = None
        cur.execute("SELECT COUNT(*), SUM(total_harga) FROM bookings")
        count, total = cur.fetchone()


    cur.execute("""
        SELECT MONTH(checkin) AS bulan, COUNT(*) AS jumlah
        FROM bookings
        WHERE YEAR(checkin) = YEAR(CURDATE())
        GROUP BY bulan
        ORDER BY bulan
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()


    bulan_dict = OrderedDict((i, 0) for i in range(1, 13))
    for b, jumlah in rows:
        bulan_dict[b] = jumlah

    labels = [calendar.month_abbr[b] for b in bulan_dict.keys()]
    values = list(bulan_dict.values())

    nama_bulan = calendar.month_name[bulan] if bulan else "Semua"

    return render_template('admin_stats.html',
                           total_pemesanan=count,
                           total_pendapatan="Rp {:,}".format(total).replace(",", ".") if total else "Rp 0",
                           chart_labels=labels,
                           chart_values=values,
                           bulan_aktif=bulan,
                           nama_bulan=nama_bulan)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html') 

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('profile.html')


@app.route('/get_available_villas', methods=['POST'])
def get_available_villas():
    data = request.get_json()
    tipe_villa = data.get('tipe_villa')
    checkin = data.get('checkin')
    checkout = data.get('checkout')

    try:
        t_checkin = datetime.strptime(checkin, "%Y-%m-%d")
        t_checkout = datetime.strptime(checkout, "%Y-%m-%d")
    except Exception:
        return jsonify({"error": "Format tanggal salah"}), 400

    if t_checkout <= t_checkin:
        return jsonify({"error": "Tanggal checkout harus setelah checkin"}), 400

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT nomor_villa FROM villas WHERE tipe_villa = %s", (tipe_villa,))
    semua_villa = [row['nomor_villa'] for row in cur.fetchall()]

    cur.execute("""
        SELECT no_villa FROM bookings 
        WHERE tipe_villa = %s
        AND (
            (checkin <= %s AND checkout > %s) OR
            (checkin < %s AND checkout >= %s) OR
            (checkin >= %s AND checkout <= %s)
        )
    """, (tipe_villa, checkin, checkin, checkout, checkout, checkin, checkout))
    booked_villas = [row['no_villa'] for row in cur.fetchall()]

    available_villas = [v for v in semua_villa if v not in booked_villas]

    cur.close()
    db.close()

    return jsonify({"available_villas": available_villas})

def generate_kode_booking(prefix="VS", length=6):
    return f"{prefix}-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()

        nama = request.form['nama']
        identitas = encrypt(request.form['identitas'])

        kamar_raw = request.form['kamar']
        if " - " not in kamar_raw:
            return "Format tipe villa salah.", 400
        kamar_name, harga_str = kamar_raw.split(" - ")
        harga_per_malam = int(harga_str)

        no_villa = int(request.form['no_villa'])

        checkin = request.form['checkin']
        checkout = request.form['checkout']

        t_checkin = datetime.strptime(checkin, "%Y-%m-%d")
        t_checkout = datetime.strptime(checkout, "%Y-%m-%d")
        lama_inap = (t_checkout - t_checkin).days
        if lama_inap <= 0:
            return "Tanggal checkout harus setelah checkin.", 400

        total_harga = harga_per_malam * lama_inap
        
        cur.execute("""
            SELECT COUNT(*) FROM bookings 
            WHERE tipe_villa = %s AND no_villa = %s
            AND (
                (checkin <= %s AND checkout > %s) OR
                (checkin < %s AND checkout >= %s) OR
                (checkin >= %s AND checkout <= %s)
            )
        """, (kamar_name, no_villa, checkin, checkin, checkout, checkout, checkin, checkout))
        (count,) = cur.fetchone()
        if count > 0:
            cur.close()
            db.close()
            return "Nomor villa sudah dipesan pada tanggal tersebut.", 400

        kode_booking = generate_kode_booking()
        cur.execute("""
            INSERT INTO bookings 
            (user_id, nama, identitas, tipe_villa, harga_per_malam, no_villa, checkin, checkout, lama_inap, total_harga, kode_booking)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (session['user_id'], nama, identitas, kamar_name, harga_per_malam, no_villa,
              checkin, checkout, lama_inap, total_harga, kode_booking))

        db.commit()
        cur.close()
        db.close()
        return redirect('/riwayat')

    return render_template('booking.html')

@app.route('/riwayat')
def riwayat():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings WHERE user_id = %s ORDER BY checkin DESC", (session['user_id'],))
    data = cur.fetchall()
    cur.close()
    db.close()

    decrypted_data = []
    for d in data:
        identitas_asli = decrypt(d['identitas'])

        lama_inap = (d['checkout'] - d['checkin']).days

        decrypted_data.append({
            'id': d['id'],
            'nama': d['nama'],
            'identitas': identitas_asli,
            'tipe_villa': d['tipe_villa'],
            'no_villa': d['no_villa'],
            'checkin': d['checkin'].strftime("%Y-%m-%d"),
            'checkout': d['checkout'].strftime("%Y-%m-%d"),
            'lama_inap': lama_inap,
            'harga_per_malam': d['harga_per_malam'],
            'total_harga': d['total_harga']
        })

    return render_template('riwayat.html', bookings=decrypted_data)


@app.route('/tiket/<int:booking_id>')
def tiket(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings WHERE id = %s AND user_id = %s", (booking_id, session['user_id']))
    data = cur.fetchone()
    cur.close()
    db.close()

    if not data:
        return "Data tidak ditemukan atau tidak diizinkan", 404

    identitas_asli = decrypt(data['identitas'])
    identitas_masked = 'X' * (len(identitas_asli) - 4) + identitas_asli[-4:]

    return render_template('tiket.html', 
    nama=data['nama'],
    identitas=identitas_masked,
    tipe_villa=data['tipe_villa'],
    no_villa=data['no_villa'],
    checkin=data['checkin'].strftime("%d/%m/%Y"),
    checkout=data['checkout'].strftime("%d/%m/%Y"),
    total_harga="Rp {:,}".format(data['total_harga']).replace(",", "."),
    booking_id=booking_id,
    kode_booking=data['kode_booking']
)


@app.route('/unduh_tiket/<int:booking_id>')
def unduh_tiket_pdf(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings WHERE id = %s AND user_id = %s", (booking_id, session['user_id']))
    data = cur.fetchone()
    cur.close()
    db.close()

    if not data:
        return "Data tidak ditemukan", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    style_title = ParagraphStyle(
        name='CustomTitle',
        fontSize=20,
        alignment=1,
        textColor=colors.HexColor("#e0aaff"),
        spaceAfter=20
    )

    content = []

    try:
        logo_path = os.path.join("static", "img", "logo.png")
        logo = ImageReader(logo_path)
        content.append(Image(logo, width=100, height=40))
        content.append(Spacer(1, 10))
    except:
        pass


    content.append(Paragraph("🎫 VillaShield", style_title))
    content.append(Spacer(1, 20))

    data_tiket = [
        ["Kode Booking", data['kode_booking']],
        ["Tipe Villa", f"{data['tipe_villa']} - No. {data['no_villa']}"],
        ["Check-in", data['checkin'].strftime('%d/%m/%Y')],
        ["Check-out", data['checkout'].strftime('%d/%m/%Y')],
    ]

    table = Table(data_tiket, colWidths=[6 * cm, 14 * cm])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#e0aaff")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2e2e3e")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [
            colors.HexColor("#2e2e3e"), colors.HexColor("#1e1e2f")
        ]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9a1750")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    qr_data = f"VillaShield Booking: {data['kode_booking']}"
    qr_img = qrcode.make(qr_data)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    content.append(Spacer(1, 10))
    content.append(Image(qr_buffer, width=100, height=100))
    content.append(Spacer(1, 20))

    footer = Paragraph(
        "<i>Terima kasih telah memesan di <b>VillaShield</b> 💜</i>",
        ParagraphStyle(name='Footer', alignment=1, textColor=colors.HexColor("#9a1750"), fontSize=12)
    )
    content.append(footer)

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="tiket_villashield.pdf", mimetype='application/pdf')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
