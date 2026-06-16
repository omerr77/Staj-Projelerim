<?php
include("db.php");

if(isset($_POST["kaydet"])){

    $ad = $_POST["oyuncu"];
    $skor = $_POST["skor"];

    $sql = "INSERT INTO skorlar(oyuncu_adi, skor)
            VALUES('$ad','$skor')";

    $baglanti->query($sql);
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Skor Kaydet</title>
</head>
<body>

<h2>Skor Kaydet</h2>

<form method="post">

Oyuncu Adı:
<input type="text" name="oyuncu" required>

<br><br>

Skor:
<input type="number" name="skor" required>

<br><br>

<button name="kaydet">Kaydet</button>

</form>

<hr>

<h2>En Yüksek Skorlar</h2>

<?php

$listele = $baglanti->query(
"SELECT * FROM skorlar ORDER BY skor DESC"
);

while($satir = $listele->fetch_assoc()){

    echo $satir["oyuncu_adi"] .
    " - " .
    $satir["skor"] .
    "<br>";
}

?>

</body>
</html>

