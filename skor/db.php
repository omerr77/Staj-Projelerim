<?php

$baglanti = new mysqli("localhost", "root", "", "oyun_skor");

if($baglanti->connect_error){
    die("Bağlantı hatası");
}

?>