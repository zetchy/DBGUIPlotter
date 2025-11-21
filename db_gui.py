import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

class theAPP:
    def __init__(self,root):
        self.root=root
        self.root.title("DOS and Band Structure Plotter")
        self.root.geometry("800x400")
        self.dos_path=None
        self.bands_path=None
        tk.Label(root, text ="Minimum energy to read (eV)").grid(row=0,column=0,sticky="e")
        self.entry_emin=tk.Entry(root)
        self.entry_emin.grid(row=0,column=1)
        tk.Label(root,text="Maximum energy to read (eV)").grid(row=1,column=0,sticky="e")
        self.entry_emax=tk.Entry(root)
        self.entry_emax.grid(row=1,column=1)
        tk.Button(root,text="Choose DOS file",command=self.load_dos).grid(row=2,column=0,sticky="e")
        self.dos_entry=tk.Entry(root,width=50,state="readonly")
        self.dos_entry.grid(row=2,column=1,sticky="e")
        tk.Button(root,text="Choose Bands file",command=self.load_bands).grid(row=3,column=0,sticky="e")
        self.bands_entry=tk.Entry(root,width=50,state="readonly")
        self.bands_entry.grid(row=3,column=1,sticky="e")
        tk.Button(root,text="Plot",command=self.plot).grid(row=4,column=1,sticky="w")
      
    def load_dos(self):
        path = filedialog.askopenfilename(filetypes=[("DOS files","*.dos")])
        if path:
            self.dos_path=path
            self.set_entry(self.dos_entry,path)

    def load_bands(self):
        path = filedialog.askopenfilename(filetypes=[("BANDS files","*.gnu")])
        if path:
            self.bands_path=path
            self.set_entry(self.bands_entry,path)

    def set_entry(self,entry_widget,text):
        entry_widget.config(state="normal")
        entry_widget.delete(0,tk.END)
        entry_widget.insert(0,text)
        entry_widget.config(state="readonly")

    def plot(self):
        if not self.dos_path or not self.bands_path:
            messagebox.showerror("Error","Please load both files")
            return
        try:
            E_min=float(self.entry_emin.get())
            E_max=float(self.entry_emax.get())
        except ValueError:
            messagebox.showerror("Error","Enter valid energy boundaries.")
            return
        dos_data=np.loadtxt(self.dos_path, comments="#")
        dos_energy=dos_data[:,0]
        dos=dos_data[:,1]
        bands_data=np.loadtxt(self.bands_path, comments="#")
        kpoints=np.unique(bands_data[:,0])
        num_k=len(kpoints)
        num_bands=len(bands_data)//num_k
        bands=np.reshape(bands_data[:,1],(num_bands,num_k))

        fig, (ax_dos,ax_bands)=plt.subplots(
            nrows=1,ncols=2,sharey=True,
            gridspec_kw={'width_ratios':[1,1],'wspace':0})
        filter_dos=(dos_energy>=E_min)&(dos_energy<=E_max)
        ax_dos.plot(dos[filter_dos],dos_energy[filter_dos],color='b',linewidth=2)
        for band in bands:
            filter_visible=(band>=E_min) &(band<=E_max)
            ax_bands.plot(kpoints,band,color='k',alpha=0.2)
            ax_bands.plot(kpoints[filter_visible],band[filter_visible],color='k',alpha=0.9,linewidth=2)

        ax_bands.set_xlabel("k-point")
        ax_bands.set_xlim(min(kpoints),max(kpoints))

        ax_dos.axhline(0,color='r',linestyle='--',linewidth=1)
        ax_bands.axhline(0,color='r',linestyle='--',linewidth=1)

        ax_dos.set_ylim(E_min,E_max)
        ax_bands.set_ylim(E_min,E_max)
        
        plt.show()

if __name__=="__main__":
    root=tk.Tk()
    app=theAPP(root)
    root.mainloop()