using System;
using System.Collections.Generic;

class Program
{
    static List<Kitap> kitaplar = new List<Kitap>();
    static int idSayac = 1;

    static void Main()
    {
        while (true)
        {
            Console.Clear();
            Console.WriteLine("KUTUPHANE UYGULAMASI");
            Console.WriteLine("1 - Kitap Ekle");
            Console.WriteLine("2 - Kitaplari Listele");
            Console.WriteLine("3 - Kitap Sil");
            Console.WriteLine("4 - Cikis");
            Console.Write("Seciminiz: ");

            string secim = Console.ReadLine();

            switch (secim)
            {
                case "1":
                    KitapEkle();
                    break;
                case "2":
                    KitaplariListele();
                    Console.ReadKey();
                    break;
                case "3":
                    KitapSil();
                    break;
                case "4":
                    return;
                default:
                    Console.WriteLine("Hatali secim!");
                    Console.ReadKey();
                    break;
            }
        }
    }

    static void KitapEkle()
    {
        Console.Clear();
        Console.Write("Kitap Adi: ");
        string kitapAdi = Console.ReadLine();

        Console.Write("Yazar: ");
        string yazar = Console.ReadLine();

        Console.Write("Sayfa Sayisi: ");
        int sayfaSayisi = int.Parse(Console.ReadLine());

        kitaplar.Add(new Kitap
        {
            Id = idSayac++,
            KitapAdi = kitapAdi,
            Yazar = yazar,
            SayfaSayisi = sayfaSayisi
        });

        Console.WriteLine("Kitap eklendi.");
        Console.ReadKey();
    }

    static void KitaplariListele()
    {
        Console.Clear();
        Console.WriteLine("KITAPLAR");

        if (kitaplar.Count == 0)
        {
            Console.WriteLine("Henuz kitap yok.");
            return;
        }

        foreach (var kitap in kitaplar)
        {
            Console.WriteLine("ID: " + kitap.Id);
            Console.WriteLine("Kitap: " + kitap.KitapAdi);
            Console.WriteLine("Yazar: " + kitap.Yazar);
            Console.WriteLine("Sayfa: " + kitap.SayfaSayisi);
            Console.WriteLine("-------------------");
        }
    }

    static void KitapSil()
    {
        Console.Clear();

        if (kitaplar.Count == 0)
        {
            Console.WriteLine("Silinecek kitap yok.");
            Console.ReadKey();
            return;
        }

        KitaplariListele();

        Console.Write("Silinecek kitap ID: ");
        int id = int.Parse(Console.ReadLine());

        Kitap silinecek = kitaplar.Find(k => k.Id == id);

        if (silinecek != null)
        {
            kitaplar.Remove(silinecek);
            Console.WriteLine("Kitap silindi.");
        }
        else
        {
            Console.WriteLine("Kitap bulunamadi.");
        }

        Console.ReadKey();
    }
}

class Kitap
{
    public int Id { get; set; }
    public string KitapAdi { get; set; }
    public string Yazar { get; set; }
    public int SayfaSayisi { get; set; }
}
