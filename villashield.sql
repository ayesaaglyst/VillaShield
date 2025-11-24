-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Jul 2025 pada 20.00
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `villashield`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `identitas` text DEFAULT NULL,
  `tipe_villa` varchar(100) DEFAULT NULL,
  `harga_per_malam` int(11) DEFAULT NULL,
  `no_villa` int(11) DEFAULT NULL,
  `checkin` date DEFAULT NULL,
  `checkout` date DEFAULT NULL,
  `total_harga` int(11) DEFAULT NULL,
  `lama_inap` int(11) DEFAULT NULL,
  `kode_booking` varchar(20) DEFAULT NULL,
  `status_checkout` varchar(20) DEFAULT 'Belum Checkout'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `bookings`
--

INSERT INTO `bookings` (`id`, `user_id`, `nama`, `identitas`, `tipe_villa`, `harga_per_malam`, `no_villa`, `checkin`, `checkout`, `total_harga`, `lama_inap`, `kode_booking`, `status_checkout`) VALUES
(1, 1, 'Ayesa Aglystia Pretty', 'ReJLowwMD+yYXg/z76y4dQ==::ReJLowwMD+yYXg/z76y4dVIflalZTPUa37ktMtlOvFiCtiEK7Ip0CI7P2mwrHfze', 'Royal Sunset Villa', 2500000, 3, '2025-06-30', '2025-07-01', 2500000, 1, NULL, 'Belum Checkout'),
(2, 1, 'Ayesa Aglystia sweety', 'rAqAnFeScFyL95z6PL7H2A==::rAqAnFeScFyL95z6PL7H2HcMpHZ1UJSiH4p5MkIZoj0TjFS/K9sz/LZTDQhUZlRj', 'Ocean Breeze Suite', 1800000, 1, '2025-06-11', '2025-06-16', 9000000, 5, NULL, 'Belum Checkout'),
(3, 2, 'Hwang Hyunjin', 'xminG+FiyEvU8HDvrSIc2Q==::xminG+FiyEvU8HDvrSIc2Q8Smv5+5TGM5eYChSwCfzg=', 'Tropical Budget Room', 750000, 1, '2025-06-27', '2025-06-29', 1500000, 2, NULL, 'Belum Checkout'),
(4, 1, 'Ayeeeeeeeeeeeee', 'tj4fDabaQ+WB2/nR712gqw==::tj4fDabaQ+WB2/nR712gq9THoHfRNSqu45XiMKveGPTq1EMfZEcLU02HnfgqKJRr', 'Garden View Cottage', 1200000, 1, '2025-07-09', '2025-07-11', 2400000, 2, NULL, 'Belum Checkout'),
(5, 1, 'Ayesa Aglystia', 'gwF33NO8RXr3POy43bsnNg==::gwF33NO8RXr3POy43bsnNkMnCVHOrNyg3MyFj22NcQc=', 'Garden View Cottage', 1200000, 2, '2025-06-26', '2025-07-11', 18000000, 15, NULL, 'Belum Checkout'),
(6, 4, 'Jaan', 'fOxVjXn1ldUDRchDRf9Tkg==::fOxVjXn1ldUDRchDRf9Tkihsf/j1AXDuOavV/ioqfmk=', 'Tropical Budget Room', 750000, 4, '2025-06-27', '2025-06-29', 1500000, 2, NULL, 'Belum Checkout'),
(7, 5, 'Syifa Tania', 'V0w7dhSNKF7JqLfSUfubkg==::V0w7dhSNKF7JqLfSUfubkiryYVOhcj49dlTlIROzJ/U=', 'Garden View Cottage', 1200000, 1, '2025-06-27', '2025-06-28', 1200000, 1, NULL, 'Belum Checkout'),
(8, 1, 'Ayesa', 'ULRKg4HWkYhdW1QzRPiR8w==::ULRKg4HWkYhdW1QzRPiR8/qifnYvmZeiLG/WnnP67y2cJaLTMcGP8pxt0qush4jq', 'Ocean Breeze Suite', 1800000, 1, '2025-06-18', '2025-06-19', 1800000, 1, 'VS-V2QF7W', 'Belum Checkout'),
(9, 1, 'Ayesa ', 'IsScf42oIdnOGMM3uFygiw==::IsScf42oIdnOGMM3uFygi/UaPknG0DrxuPrpz0+RIaw=', 'Garden View Cottage', 1200000, 4, '2025-06-30', '2025-07-02', 2400000, 2, 'VS-W3QS2P', 'Belum Checkout'),
(10, 7, 'Jun Hui', 'DojTP4UdF44G63k/1H0+HA==::DojTP4UdF44G63k/1H0+HFHtMBfv3TDHM21OZ3ngztY=', 'Royal Sunset Villa', 2500000, 3, '2025-07-04', '2025-07-06', 5000000, 2, 'VS-4ZFF02', 'Belum Checkout'),
(11, 8, 'Azmi', 'YS4PLu8lX426VzZzY1+U9Q==::YS4PLu8lX426VzZzY1+U9XPZUkWW/QZmPvw/dWSpPLw=', 'Garden View Cottage', 1200000, 3, '2025-07-26', '2025-07-30', 4800000, 4, 'VS-PL5YVP', 'Belum Checkout'),
(12, 8, 'Azmi', 'LY5czzhbcO2J44YMRPfAKw==::LY5czzhbcO2J44YMRPfAK0T7oWre9SMbHdrAfv1FrCw=', 'Tropical Budget Room', 750000, 3, '2025-07-30', '2025-07-31', 750000, 1, 'VS-B6CDZW', 'Belum Checkout'),
(13, 8, 'Azmi', '1dDGjxsHYbm58zwi/VJKBg==::1dDGjxsHYbm58zwi/VJKBqQhJNLX5Deq/Wrd31s/THk=', 'Garden View Cottage', 1200000, 2, '2025-07-29', '2025-07-31', 2400000, 2, 'VS-E6ZFUP', 'Sudah Checkout'),
(14, 9, 'Syifa', 'S1/TXQZMJi9M1+CygTDMrw==::S1/TXQZMJi9M1+CygTDMrwSc/aXpVeEL6y4uihUHvEQ=', 'Ocean Breeze Suite', 1800000, 2, '2025-07-29', '2025-07-30', 1800000, 1, 'VS-I4XUVZ', 'Belum Checkout'),
(15, 9, 'Syifa', 'bwSJAGM+edEDHrhFudXNeg==::bwSJAGM+edEDHrhFudXNekY0HZQj+Zd/dgJktjj3uKY=', 'Garden View Cottage', 1200000, 3, '2025-07-16', '2025-07-18', 2400000, 2, 'VS-2MV5DH', 'Belum Checkout'),
(16, 9, 'Syifa', '0Ld9DlmQrRDZnT2uAjFM5w==::0Ld9DlmQrRDZnT2uAjFM5w4YmUqQya/gBKgRKjxG2Jk=', 'Tropical Budget Room', 750000, 3, '2025-07-29', '2025-07-30', 750000, 1, 'VS-Z0FUAF', 'Belum Checkout'),
(17, 10, 'Azhar Bintang', 'DfziOfP8aiX8ImJr8Pyycw==::DfziOfP8aiX8ImJr8PyyczKBX/JiEuaJ2T0v5NK8tMY=', 'Garden View Cottage', 1200000, 4, '2025-07-29', '2025-07-31', 2400000, 2, 'VS-2PIBAF', 'Belum Checkout'),
(18, 15, 'Tamu 1', '0N/9wF0Rd+FQ9np2M4s1zw==::0N/9wF0Rd+FQ9np2M4s1z1O9N8gi8z03luV5sJOGubeFu7qHyieKoud+KE3gj8Kg', 'Ocean Breeze Suite', 1800000, 2, '2025-07-13', '2025-07-14', 1800000, 1, 'VS-HQRZWN', 'Belum Checkout'),
(19, 15, 'tamu 2', 'FZA2mbq+uoYDML92EUJtSw==::FZA2mbq+uoYDML92EUJtS7kSG4ZgGDFl4PrVNFfwW5i/hDTdgOYxpJRTI1x28k3m', 'Tropical Budget Room', 750000, 3, '2025-07-24', '2025-07-26', 1500000, 2, 'VS-9PW8TW', 'Belum Checkout'),
(20, 1, 'Ayesa Cantik', 'Ps/FijDn3e93qLWH2H3TIw==::Ps/FijDn3e93qLWH2H3TI/o/GFpPAl6gqx/UWMp5uRc=', 'Tropical Budget Room', 750000, 1, '2025-07-30', '2025-08-09', 7500000, 10, 'VS-8G4LV7', 'Belum Checkout');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'user',
  `is_deleted` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `NAME`, `email`, `pass`, `role`, `is_deleted`) VALUES
(1, 'Ayesa Aglystia', 'aye@gmail.com', '$2b$12$f9AB1F.q/12tqjhG8bUkp.JKXStpPhqf/sULEmoJ8oz3heV432l.6', 'user', 0),
(2, 'Hwang Hyunjin', 'hyunjin@gmail.com', '$2b$12$PT10T7ExwM7/u3TuMrTi/ODIqGQ6oIdA7Ejbz0wAb4KkZWS6AnGBm', 'user', 0),
(3, 'Abdurrahman', 'abdurrahman@gmail.com', '$2b$12$xeVo7jhD.NTE6ArJ2Q1GtusKzrt1SIDGnM.gR2HF7Ql5nxP9SyBpa', 'user', 0),
(4, 'Jaan', 'jaan@gmail.com', '$2b$12$54rTX5sDCrwofVorjlDMseoEfRB29deecOpamXNkFXIBDXck1Xp36', 'user', 1),
(5, 'Syifa Tania', 'syifa@gmail.com', '$2b$12$zrHWWU6qQ3tDXiHuO6jhruPSHcGn935ipJr4vfIAb20eiXRrIB2du', 'user', 0),
(6, 'Ayat Akras', 'aca@gmail.com', '$2b$12$32SloaWp8v7qIhCbklZpnOHnDz4H12AaUfUMKxSc9KJnd3S25.dhS', 'user', 0),
(7, 'Moon Junhui', 'jun@gmail.com', '$2b$12$GgLkPZoktkmo8HLrOwAgfuZtMo.KU5GQXUcgzt898DJR7BmBGqd.K', 'user', 0),
(8, 'Azmi', 'azmi@gmail.com', '$2b$12$8Ih8.buLzzi15dkTSHdasOol7WxaMtKCPXorLQPwDpghEm8DnFGpG', 'user', 0),
(9, 'Syifa', 'syifa2@gmail.com', '$2b$12$.RaSWp3b6WH6HhDkTxjrd.VW3p828agBFblYJoEyW579kCvAnH8s6', 'user', 0),
(10, 'Azhar Bintang', 'bintang@gmail.com', '$2b$12$0vgbudJCQLJ1U29RpYn7tO3LD37EifiQluG9wZHr1ryE8H1YY9iZ6', 'user', 0),
(14, 'Admin', 'admin@gmail.com', '$2b$12$73OhVRPPklhbpEjirOFrnO4DhuhBEXUoZrFvmtls.8enxJyyjmLvC', 'admin', 0),
(15, 'Guest User', 'guest@villa.com', 'guest123', 'guest', 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `villas`
--

CREATE TABLE `villas` (
  `id` int(11) NOT NULL,
  `tipe_villa` varchar(100) DEFAULT NULL,
  `nomor_villa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `villas`
--

INSERT INTO `villas` (`id`, `tipe_villa`, `nomor_villa`) VALUES
(1, 'Royal Sunset Villa', 1),
(2, 'Royal Sunset Villa', 2),
(3, 'Royal Sunset Villa', 3),
(4, 'Ocean Breeze Suite', 1),
(5, 'Ocean Breeze Suite', 2),
(6, 'Garden View Cottage', 1),
(7, 'Garden View Cottage', 2),
(8, 'Garden View Cottage', 3),
(9, 'Garden View Cottage', 4),
(10, 'Tropical Budget Room', 1),
(11, 'Tropical Budget Room', 2),
(12, 'Tropical Budget Room', 3),
(13, 'Tropical Budget Room', 4),
(14, 'Tropical Budget Room', 5);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kode_booking` (`kode_booking`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indeks untuk tabel `villas`
--
ALTER TABLE `villas`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT untuk tabel `villas`
--
ALTER TABLE `villas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
