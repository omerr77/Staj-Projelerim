#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Video İndirici
Kullanıcının girdiği YouTube video linkinden videoyu farklı çözünürlüklerde indirir.
"""

import sys
import os
import re

try:
    import yt_dlp
except ImportError:
    print("✗ yt-dlp kütüphanesi bulunamadı!")
    print("Lütfen şu komutu çalıştırın: pip install yt-dlp")
    sys.exit(1)


def print_banner():
    """Program başlığını yazdırır."""
    print("=" * 60)
    print("     YouTube Video İndirici")
    print("=" * 60)
    print()


def validate_and_normalize_url(url):
    """YouTube URL'sini doğrular ve normalize eder."""
    if not url:
        return None
    
    url = url.strip()
    
    # YouTube URL pattern'leri
    patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|m\.youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'([a-zA-Z0-9_-]{11})',  # Sadece video ID
    ]
    
    video_id = None
    
    # URL'den video ID'yi çıkar
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1) if match.groups() else match.group(0)
            break
    
    if not video_id or len(video_id) != 11:
        return None
    
    # Standart YouTube URL formatına çevir
    normalized_url = f"https://www.youtube.com/watch?v={video_id}"
    return normalized_url


def get_video_url():
    """Kullanıcıdan YouTube video URL'sini alır."""
    while True:
        url = input("YouTube video linkini girin: ").strip()
        
        if not url:
            print("✗ Hata: Link boş olamaz!")
            continue
        
        # URL'yi doğrula ve normalize et
        normalized_url = validate_and_normalize_url(url)
        
        if normalized_url:
            # Eğer kullanıcı sadece ID girmişse, tam URL'yi göster
            if url != normalized_url and len(url) == 11:
                print(f"✓ URL algılandı: {normalized_url}")
            return normalized_url
        else:
            print("✗ Geçersiz YouTube linki!")
            print("\nGeçerli link formatları:")
            print("  - https://www.youtube.com/watch?v=VIDEO_ID")
            print("  - https://youtu.be/VIDEO_ID")
            print("  - https://youtube.com/watch?v=VIDEO_ID")
            print("  - VIDEO_ID (sadece 11 karakterlik ID)")
            
            retry = input("\nTekrar denemek ister misiniz? (e/h): ").strip().lower()
            if retry != 'e':
                sys.exit(1)


def get_video_info(url):
    """Video bilgilerini alır."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if 'Private video' in error_msg or 'private' in error_msg.lower():
            print("\n✗ Hata: Bu video özel (private) ve erişilemiyor!")
        elif 'Video unavailable' in error_msg or 'unavailable' in error_msg.lower():
            print("\n✗ Hata: Video bulunamadı veya erişilemiyor!")
        elif 'Age-restricted' in error_msg or 'age' in error_msg.lower():
            print("\n✗ Hata: Bu video yaş sınırlamalı!")
        elif 'Sign in' in error_msg or 'login' in error_msg.lower():
            print("\n✗ Hata: Bu video için giriş yapmanız gerekiyor!")
        else:
            print(f"\n✗ Hata: {error_msg[:200]}")
        return None
    except Exception as e:
        print(f"\n✗ Beklenmeyen hata: {str(e)}")
        return None


def get_available_formats(info):
    """Mevcut formatları listeler."""
    if not info or 'formats' not in info:
        return []
    
    formats = []
    seen_resolutions = set()
    
    for fmt in info.get('formats', []):
        # Sadece video formatlarını al
        if fmt.get('vcodec') != 'none' and fmt.get('resolution'):
            res = fmt.get('resolution', 'unknown')
            if res not in seen_resolutions:
                seen_resolutions.add(res)
                formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext', 'mp4'),
                    'resolution': res,
                    'filesize': fmt.get('filesize'),
                    'format_note': fmt.get('format_note', '')
                })
    
    # Çözünürlüğe göre sırala
    def parse_resolution(res):
        match = re.search(r'(\d+)', res)
        return int(match.group(1)) if match else 0
    
    formats.sort(key=lambda x: parse_resolution(x['resolution']), reverse=True)
    return formats


def display_formats(formats):
    """Formatları kullanıcıya gösterir."""
    if not formats:
        print("\nMevcut formatlar alınamadı. Varsayılan yüksek kalite kullanılacak.")
        return None
    
    print("\nMevcut çözünürlükler ve formatlar:")
    print("-" * 60)
    
    for i, fmt in enumerate(formats, 1):
        size_str = ""
        if fmt['filesize']:
            size_mb = fmt['filesize'] / (1024 * 1024)
            size_str = f" - {size_mb:.2f} MB"
        
        print(f"{i}. {fmt['resolution']} - {fmt['ext']}{size_str}")
    
    return formats


def select_format(formats):
    """Kullanıcıdan format seçimi alır."""
    if not formats:
        return None
    
    while True:
        try:
            choice = input(f"\nİndirmek istediğiniz formatı seçin (1-{len(formats)}, Enter=En yüksek kalite): ").strip()
            
            if not choice:
                # En yüksek kalite
                return formats[0]['format_id']
            
            choice = int(choice)
            if 1 <= choice <= len(formats):
                return formats[choice - 1]['format_id']
            else:
                print(f"Lütfen 1 ile {len(formats)} arasında bir sayı girin!")
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
        except KeyboardInterrupt:
            print("\n\nİşlem iptal edildi.")
            sys.exit(0)


def get_download_path():
    """İndirme klasörünü belirler."""
    # Varsayılan klasörü belirle
    home = os.path.expanduser("~")
    downloads_paths = [
        os.path.join(home, "Downloads"),
        os.path.join(home, "İndirilenler"),
        os.path.join(home, "Masaüstü"),
        os.path.join(os.getcwd(), "downloads")
    ]
    
    default_path = None
    for path in downloads_paths:
        if os.path.exists(path) and os.path.isdir(path):
            default_path = path
            break
    
    # Hiçbiri yoksa mevcut klasörde downloads oluştur
    if not default_path:
        default_path = os.path.join(os.getcwd(), "downloads")
    
    print(f"\n{'='*60}")
    print("İNDİRME KLASÖRÜ SEÇİMİ")
    print(f"{'='*60}")
    print(f"\nVarsayılan klasör: {default_path}")
    print("\nSeçenekler:")
    print("1. Varsayılan klasörü kullan (Enter)")
    print("2. Farklı bir klasör belirle (f)")
    print("3. Mevcut klasörü kullan (m)")
    
    choice = input("\nSeçiminiz (Enter/f/m): ").strip().lower()
    
    if choice == 'f':
        while True:
            custom_path = input("\nKlasör yolunu girin: ").strip()
            if not custom_path:
                print("Klasör yolu boş olamaz!")
                continue
            
            # Tırnak işaretlerini temizle
            custom_path = custom_path.strip('"\'')
            
            # Klasörü oluştur
            try:
                os.makedirs(custom_path, exist_ok=True)
                if os.path.isdir(custom_path):
                    print(f"✓ Klasör hazır: {custom_path}")
                    return custom_path
                else:
                    print("✗ Geçersiz klasör yolu!")
            except Exception as e:
                print(f"✗ Klasör oluşturulamadı: {str(e)}")
                retry = input("Tekrar denemek ister misiniz? (e/h): ").strip().lower()
                if retry != 'e':
                    return default_path
    
    elif choice == 'm':
        current_path = os.getcwd()
        print(f"✓ Mevcut klasör kullanılacak: {current_path}")
        return current_path
    
    # Varsayılan
    print(f"✓ Varsayılan klasör kullanılacak: {default_path}")
    return default_path


def sanitize_filename(filename):
    """Dosya adındaki geçersiz karakterleri temizler."""
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def download_video(url, format_id, download_path, video_title):
    """Videoyu indirir."""
    try:
        # Klasörü oluştur
        os.makedirs(download_path, exist_ok=True)
        
        # Dosya adını temizle
        safe_title = sanitize_filename(video_title)
        output_template = os.path.join(download_path, f'{safe_title}.%(ext)s')
        
        print(f"\nİndiriliyor: {video_title}")
        print(f"Klasör: {download_path}")
        print("-" * 60)
        
        # yt-dlp seçenekleri
        ydl_opts = {
            'format': format_id if format_id else 'best',
            'outtmpl': output_template,
            'noplaylist': True,
            'progress_hooks': [download_progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("\n\n✓ İndirme tamamlandı!")
        print(f"Video şu klasöre kaydedildi: {download_path}")
        
        # İndirilen dosyayı bul
        files = os.listdir(download_path)
        video_files = [f for f in files if f.startswith(safe_title) and 
                      f.endswith(('.mp4', '.webm', '.mkv', '.m4a', '.mp3'))]
        if video_files:
            print(f"İndirilen dosya: {video_files[0]}")
            
    except KeyboardInterrupt:
        print("\n\nİşlem iptal edildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ İndirme sırasında hata oluştu: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def download_progress_hook(d):
    """İndirme ilerlemesini gösterir."""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            print(f"\rİndiriliyor: %{percent:.1f} - {d['_percent_str']} - {d['_speed_str']}", end='', flush=True)
        elif '_percent_str' in d:
            print(f"\rİndiriliyor: {d['_percent_str']} - {d['_speed_str']}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\r✓ İndirme tamamlandı!                    ")


def main():
    """Ana program fonksiyonu."""
    print_banner()
    
    try:
        # Video URL'sini al
        url = get_video_url()
        
        # Video bilgilerini al
        print("\nVideo bilgileri alınıyor...")
        info = get_video_info(url)
        
        if not info:
            print("\n✗ Video bilgileri alınamadı!")
            print("Lütfen YouTube linkinin doğru olduğundan emin olun.")
            sys.exit(1)
        
        # Video bilgilerini göster
        title = info.get('title', 'Bilinmiyor')
        uploader = info.get('uploader', 'Bilinmiyor')
        duration = info.get('duration', 0)
        view_count = info.get('view_count', 0)
        
        print(f"\nVideo Başlığı: {title}")
        print(f"Kanal: {uploader}")
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            print(f"Süre: {minutes}:{seconds:02d}")
        if view_count:
            print(f"İzlenme Sayısı: {view_count:,}")
        
        # Formatları al ve göster
        formats = get_available_formats(info)
        display_formats(formats)
        
        # Format seçimi
        format_id = select_format(formats) if formats else None
        
        # İndirme klasörünü belirle
        download_path = get_download_path()
        
        # Videoyu indir
        download_video(url, format_id, download_path, title)
        
    except KeyboardInterrupt:
        print("\n\nİşlem iptal edildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Beklenmeyen bir hata oluştu: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
