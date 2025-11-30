import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class Model():
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Model, cls).__new__(cls)
            cls.services = {
                'Sedan': {'harga': 1000000},
                'SUV': {'harga': 900000},
                'Truck': {'harga': 2000000},
                'MPV': {'harga': 1500000},
                'Off-road': {'harga': 1900000},
                'Pickup': {'harga': 500000},
            }
        return cls._instance

class View():
    def __init__(self, root):
        self.root = root
        self.root.title("Rental Mobil")
        
        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label_services = ttk.Label(self.frame, text="BimBim Rental", font=("Helvetica", 14, "bold"))
        self.label_services.grid(row=0, column=0, columnspan=3, pady=(5, 0))

        self.label_instruction = ttk.Label(self.frame, text="Silahkan pilih mobil sesuai dengan keinginan anda")
        self.label_instruction.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        self.frame.grid_rowconfigure(4, weight=1)
        
        self.exit_button = ttk.Button(self.frame, text="Keluar", command=self.keluar_aplikasi)
        self.exit_button.grid(row=5, column=2, pady=(20, 10), sticky="e")

    def daftar_layanan(self, services):
        for nomor, (x, y) in enumerate(services.items(), start=0):
            button = ttk.Button(self.frame, text=x, command=lambda x=x: self.menu_rental(x), width=20)
            button.grid(row=(nomor // 3) + 3, column=(nomor % 3), padx=10, pady=10)

    def menu_rental(self, selected_service):
        self.root.withdraw()
        rental_window = tk.Toplevel(self.root)
        rental_window.title("Rental")

        frame = ttk.Frame(rental_window, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        harga = Model().services[selected_service]['harga']

        ttk.Label(frame, text=f"Tipe Mobil {selected_service}", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text=f"Harga per hari: Rp{harga:,.0f}".replace(',', '.')).grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="Jumlah mobil:").grid(row=2, column=0, pady=5)
        jumlah_mobil_entry = ttk.Entry(frame)
        jumlah_mobil_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Lama rental (hari):").grid(row=3, column=0, pady=5)
        lama_rental_entry = ttk.Entry(frame)
        lama_rental_entry.grid(row=3, column=1, pady=5)

        def submit_rental():
            jumlah_mobil_str = jumlah_mobil_entry.get()
            lama_rental_str = lama_rental_entry.get()

            if jumlah_mobil_str.isdigit() and lama_rental_str.isdigit():
                jumlah_mobil = int(jumlah_mobil_str)
                lama_rental = int(lama_rental_str)

                if jumlah_mobil > 0 and lama_rental > 0:
                    jenis_mobil, jumlah_mobil, lama_rental, harga_total = RentalFactory.proses_hitung_rental(selected_service, jumlah_mobil, lama_rental)
                    self.tampilkan_nota(jenis_mobil, jumlah_mobil, lama_rental, harga_total, rental_window)
                    rental_window.withdraw()
                else:
                    messagebox.showerror("Error", "Input tidak valid. Masukkan jumlah mobil dan lama rental yang valid.")

            else:
                messagebox.showerror("Error", "Input tidak valid. Masukkan jumlah mobil dan lama rental yang valid.")

        def kembali_ke_menu_utama():
            self.root.deiconify()
            rental_window.destroy()

        ttk.Button(frame, text="Kembali", command=kembali_ke_menu_utama).grid(row=4, column=0, pady=10, padx=(5, 10), sticky="w")
        ttk.Button(frame, text="Lanjutkan", command=submit_rental).grid(row=4, column=1, pady=10, padx=(5, 10), sticky="e")

    def tampilkan_nota(self, jenis_mobil, jumlah_mobil, lama_rental, harga_total, rental_window):
        nota_window = tk.Toplevel(self.root)
        nota_window.title("Nota Rental Mobil")

        frame = ttk.Frame(nota_window, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Nota Penyewaan Mobil", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=10)

        ttk.Label(frame, text="Rincian:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="w")

        ttk.Label(frame, text="Jenis Mobil", font=("Helvetica", 10, "bold")).grid(row=2, column=0, pady=5, padx=10, sticky="w")
        ttk.Label(frame, text=f"=  {jenis_mobil}").grid(row=2, column=1, pady=5, padx=10, sticky="w")

        ttk.Label(frame, text="Jumlah Mobil", font=("Helvetica", 10, "bold")).grid(row=3, column=0, pady=5, padx=10, sticky="w")
        ttk.Label(frame, text=f"=  {jumlah_mobil}").grid(row=3, column=1, pady=5, padx=10, sticky="w")

        ttk.Label(frame, text="Lama Rental (hari)", font=("Helvetica", 10, "bold")).grid(row=4, column=0, pady=5, padx=10, sticky="w")
        ttk.Label(frame, text=f"=  {lama_rental} hari").grid(row=4, column=1, pady=5, padx=10, sticky="w")

        ttk.Label(frame, text="Harga Total", font=("Helvetica", 10, "bold")).grid(row=5, column=0, pady=5, padx=10, sticky="w")
        ttk.Label(frame, text=f"=  Rp{harga_total:,.0f}".replace(',', '.'), font=("Helvetica", 10, "bold")).grid(row=5, column=1, pady=5, padx=10, sticky="w")

        ttk.Button(frame, text="Upload Bukti Pembayaran", command=self.upload_bukti_pembayaran).grid(row=6, column=0, columnspan=2, pady=10)
        
        def jendela_lokasi():
            nota_window.destroy()
            share_location_window = tk.Toplevel(self.root)
            share_location_window.title("Share Lokasi")

            share_frame = ttk.Frame(share_location_window, padding="10 10 10 10")
            share_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

            ttk.Label(share_frame, text="Silahkan share link lokasi anda", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
            link_entry = ttk.Entry(share_frame, width=30)
            link_entry.grid(row=1, column=0, pady=10)

            def submit_link():
                link = link_entry.get()
                share_location_window.destroy()
                thanks_window = tk.Toplevel(self.root)
                thanks_window.title("Terima Kasih")

                thanks_frame = ttk.Frame(thanks_window, padding="10 10 10 10")
                thanks_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

                ttk.Label(thanks_frame, text="Terima kasih telah menggunakan layanan rental mobil kami!", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=10)
                ttk.Label(thanks_frame, text="Kami akan segera mengantar mobil anda", font=("Helvetica", 12, "bold")).grid(row=1, column=0, pady=5)

                def tutup_jendela_terimakasih():
                    thanks_window.destroy()
                    self.root.deiconify()

                ttk.Button(thanks_frame, text="Kembali ke menu", command=tutup_jendela_terimakasih).grid(row=2, column=0, pady=10)

            def konfirmasi_lokasi():
                confirm_window = tk.Toplevel(self.root)
                confirm_window.title("Konfirmasi Lokasi")

                confirm_frame = ttk.Frame(confirm_window, padding="10 10 10 10")
                confirm_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

                ttk.Label(confirm_frame, text="Apakah anda yakin lokasi anda benar?", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

                def kembali_jendela_share_lokasi():
                    confirm_window.destroy()

                def melanjutkan_dari_jendela_lokasi():
                    confirm_window.destroy()
                    submit_link()

                ttk.Button(confirm_frame, text="Kembali", command=kembali_jendela_share_lokasi).grid(row=1, column=0, pady=10, padx=10)
                ttk.Button(confirm_frame, text="Ya", command=melanjutkan_dari_jendela_lokasi).grid(row=1, column=1, pady=10, padx=10)

            ttk.Button(share_frame, text="Submit", command=konfirmasi_lokasi).grid(row=1, column=1, pady=10, padx=10)
        
        def kembali_ke_jendela_rental():
            nota_window.destroy()
            rental_window.deiconify()

        ttk.Button(frame, text="Kembali", command=kembali_ke_jendela_rental).grid(row=8, column=0, pady=10, padx=(10, 5), sticky="w")
        ttk.Button(frame, text="Selesai", command=jendela_lokasi).grid(row=8, column=1, pady=10, padx=(5, 10), sticky="e")
    
    def upload_bukti_pembayaran(self):
        file_path = filedialog.askopenfilename(title="Pilih Bukti Pembayaran", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            messagebox.showinfo("Berhasil", "Bukti pembayaran berhasil diunggah.")
        else:
            messagebox.showerror("Error", "Gagal mengunggah bukti pembayaran.")

    def keluar_aplikasi(self):
        self.root.quit()

class RentalFactory():
    @staticmethod
    def proses_hitung_rental(jenis_mobil, jumlah_mobil, lama_rental):
        harga_per_hari = Model().services[jenis_mobil]['harga']
        harga_total = lama_rental * harga_per_hari * jumlah_mobil
        return jenis_mobil, jumlah_mobil, lama_rental, harga_total

class Controller():
    def __init__(self, root):
        self.model = Model() 
        self.view = View(root)
        self.eksekusi_layanan()

    def eksekusi_layanan(self):
        services = self.model.services
        self.view.daftar_layanan(services)

root = tk.Tk()
rental_mobil = Controller(root)
root.mainloop()
