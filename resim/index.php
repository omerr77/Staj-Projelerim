
<?php

if(isset($_POST["yukle"])){

    $dosya = $_FILES["resim"];

    $hedef = "uploads/" . $dosya["name"];

    move_uploaded_file(
        $dosya["tmp_name"],
        $hedef
    );

    $kaynak = imagecreatefromjpeg($hedef);

    $yeni_genislik = 150;
    $yeni_yukseklik = 150;

    $yeni_resim = imagecreatetruecolor(
        $yeni_genislik,
        $yeni_yukseklik
    );

    imagecopyresampled(
        $yeni_resim,
        $kaynak,
        0,0,0,0,
        $yeni_genislik,
        $yeni_yukseklik,
        imagesx($kaynak),
        imagesy($kaynak)
    );

    imagejpeg(
        $yeni_resim,
        "uploads/kucuk_resim.jpg"
    );

    echo "Resim başarıyla küçültüldü.";
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Resim Yükleme</title>
</head>
<body>

<form method="post"
enctype="multipart/form-data">

<input type="file"
name="resim"
required>

<button name="yukle">
Yükle
</button>

</form>

</body>
</html>
