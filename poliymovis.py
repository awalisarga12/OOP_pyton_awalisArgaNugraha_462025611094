

class Device:
    """Kelas Utama / Root Parent (Kelas A)"""
    def __init__(self, brand, **kwargs):
        super().__init__() 
        self.brand = brand
        print(f"[{self.brand}] Device Berhasil Diinisialisasi")

    def info(self):
        print(f"Brand: {self.brand}")


class Smartphone(Device):
    """Kelas Turunan Pertama - Kiri (Kelas B)"""
    def __init__(self, os, **kwargs):
        # Meneruskan argumen sisa ke kelas berikutnya dalam urutan MRO
        super().__init__(**kwargs)
        self.os = os
        print(f"Smartphone Berhasil Diinisialisasi dengan OS: {self.os}")

    def info(self):
        super().info()
        print(f"Sistem Operasi: {self.os}")


class SmartCamera(Device):
    """Kelas Turunan Pertama - Kanan (Kelas C)"""
    def __init__(self, resolution, **kwargs):
        super().__init__(**kwargs)
        self.resolution = resolution
        print(f"SmartCamera Berhasil Diinisialisasi dengan Resolusi: {self.resolution}")

    def info(self):
        super().info()
        print(f"Resolusi Kamera: {self.resolution}")


class SmartPhotoPhone(Smartphone, SmartCamera):
    """
    Kelas Turunan Kedua (Kelas D - Anak dari B dan C)
    Mendemonstrasikan Diamond Problem yang diselesaikan dengan super() dan MRO
    """
    def __init__(self, brand, os, resolution, model_name):
        super().__init__(brand=brand, os=os, resolution=resolution)
        self.model_name = model_name
        print(f"SmartPhotoPhone {self.model_name} Siap Digunakan!\n")

    def info(self):
        print(f"--- Info Produk: {self.model_name} ---")
        super().info() 


if __name__ == "__main__":
    print("=== MRO (Method Resolution Order) untuk SmartPhotoPhone ===")
    for kelas in SmartPhotoPhone.__mro__:
        print(kelas)
    print("=========================================================\n")

    # Membuat objek dari kelas Diamond (SmartPhotoPhone)
    gadget_baru = SmartPhotoPhone(
        brand="Samsung", 
        os="Android 14", 
        resolution="108 MP", 
        model_name="Galaxy Ultra Photo"
    )

    gadget_baru.info()