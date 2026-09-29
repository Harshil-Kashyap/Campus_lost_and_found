import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auth import login, register
from items import add_item, get_items, my_items, close_item, delete_item
from claims import add_claim, get_claims, set_claim
from reports import stats


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Campus Lost & Found')
        self.geometry('1050x680')
        self.minsize(900, 600)
        self.user = None
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        box = ttk.Frame(self, padding=35)
        box.place(relx=.5, rely=.5, anchor='center')
        ttk.Label(box, text='Campus Lost & Found', font=('Arial', 24, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(box, text='Find it. Report it. Return it.', font=('Arial', 11)).grid(row=1, column=0, columnspan=2, pady=(0,20))
        ttk.Label(box, text='Email').grid(row=2, column=0, sticky='w', pady=5)
        em = ttk.Entry(box, width=34); em.grid(row=2, column=1, pady=5)
        ttk.Label(box, text='Password').grid(row=3, column=0, sticky='w', pady=5)
        pw = ttk.Entry(box, show='*', width=34); pw.grid(row=3, column=1, pady=5)
        def go():
            u = login(em.get(), pw.get())
            if u:
                self.user = u; self.show_home()
            else: messagebox.showerror('Login', 'Wrong email or password.')
        ttk.Button(box, text='Login', command=go).grid(row=4, column=0, columnspan=2, pady=12, sticky='ew')
        ttk.Button(box, text='Create account', command=self.show_register).grid(row=5, column=0, columnspan=2, sticky='ew')
        ttk.Label(box, text='Demo: student@campus.local / student123').grid(row=6, column=0, columnspan=2, pady=(18,0))

    def show_register(self):
        self.clear()
        box = ttk.Frame(self, padding=35); box.place(relx=.5, rely=.5, anchor='center')
        ttk.Label(box, text='Create Student Account', font=('Arial', 21, 'bold')).grid(row=0,column=0,columnspan=2,pady=10)
        fields = {}
        for i, name in enumerate(['Name','Email','Password'], 1):
            ttk.Label(box,text=name).grid(row=i,column=0,sticky='w',pady=6)
            e=ttk.Entry(box,width=34,show='*' if name=='Password' else '')
            e.grid(row=i,column=1,pady=6); fields[name]=e
        def save():
            ok,msg=register(fields['Name'].get(),fields['Email'].get(),fields['Password'].get())
            if ok: messagebox.showinfo('Account',msg); self.show_login()
            else: messagebox.showerror('Account',msg)
        ttk.Button(box,text='Register',command=save).grid(row=4,column=0,columnspan=2,pady=10,sticky='ew')
        ttk.Button(box,text='Back to login',command=self.show_login).grid(row=5,column=0,columnspan=2,sticky='ew')

    def show_home(self):
        self.clear()
        top=ttk.Frame(self,padding=10); top.pack(fill='x')
        ttk.Label(top,text=f"Campus Lost & Found | Hi, {self.user['name']}",font=('Arial',16,'bold')).pack(side='left')
        ttk.Button(top,text='Logout',command=self.logout).pack(side='right')
        nb=ttk.Notebook(self); nb.pack(fill='both',expand=True,padx=10,pady=5)
        self.make_browse(nb)
        self.make_report(nb)
        self.make_claims(nb)
        self.make_mine(nb)
        if self.user['role']=='admin': self.make_admin(nb)

    def logout(self): self.user=None; self.show_login()

    def make_browse(self, nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text='Browse Items')
        bar=ttk.Frame(f); bar.pack(fill='x')
        ttk.Label(bar,text='Search').pack(side='left')
        q=ttk.Entry(bar,width=30); q.pack(side='left',padx=6)
        kind=tk.StringVar(value='all')
        ttk.Combobox(bar,textvariable=kind,values=['all','lost','found'],state='readonly',width=10).pack(side='left')
        tree=self.item_tree(f)
        def load():
            for x in tree.get_children(): tree.delete(x)
            k=None if kind.get()=='all' else kind.get()
            for r in get_items(k,q.get()):
                tree.insert('', 'end', values=(r['id'],r['kind'].title(),r['title'],r['cat'],r['place'],r['day'],r['status'],r['who']))
        ttk.Button(bar,text='Search',command=load).pack(side='left',padx=6)
        ttk.Button(bar,text='Refresh',command=load).pack(side='left')
        ttk.Button(f,text='Claim selected item',command=lambda:self.claim_selected(tree)).pack(pady=8)
        load()

    def item_tree(self, parent):
        cols=('ID','Type','Item','Category','Place','Date','Status','Reported by')
        tree=ttk.Treeview(parent,columns=cols,show='headings')
        for c in cols:
            tree.heading(c,text=c); tree.column(c,width=100)
        tree.column('ID',width=45); tree.column('Item',width=170); tree.pack(fill='both',expand=True,pady=10)
        return tree

    def claim_selected(self, tree):
        sel=tree.selection()
        if not sel: messagebox.showwarning('Claim','Select an item first.'); return
        vals=tree.item(sel[0])['values']; iid=vals[0]
        note=simpledialog.askstring('Claim','Why do you believe this item is yours?')
        if note:
            ok,msg=add_claim(iid,self.user['id'],note)
            messagebox.showinfo('Claim',msg) if ok else messagebox.showerror('Claim',msg)

    def make_report(self, nb):
        f=ttk.Frame(nb,padding=18); nb.add(f,text='Report Item')
        fields={}
        ttk.Label(f,text='Report a lost or found item',font=('Arial',15,'bold')).grid(row=0,column=0,columnspan=2,pady=8)
        for i,name in enumerate(['Type','Item name','Category','Place','Date (DD-MM-YYYY)','Details'],1):
            ttk.Label(f,text=name).grid(row=i,column=0,sticky='w',pady=7)
            if name=='Type':
                e=ttk.Combobox(f,values=['lost','found'],state='readonly'); e.set('lost')
            elif name=='Details': e=tk.Text(f,width=48,height=6)
            else: e=ttk.Entry(f,width=50)
            e.grid(row=i,column=1,pady=7); fields[name]=e
        def save():
            def val(x): return x.get('1.0','end').strip() if isinstance(x,tk.Text) else x.get().strip()
            vals={k:val(v) for k,v in fields.items()}
            if not all(vals.values()): messagebox.showwarning('Report','Please fill every field.'); return
            add_item(self.user['id'],vals['Type'],vals['Item name'],vals['Category'],vals['Place'],vals['Date (DD-MM-YYYY)'],vals['Details'])
            messagebox.showinfo('Report','Item reported successfully.')
            for w in fields.values():
                if isinstance(w,tk.Text): w.delete('1.0','end')
                else: w.delete(0,'end')
        ttk.Button(f,text='Submit report',command=save).grid(row=7,column=1,sticky='w',pady=12)

    def make_claims(self, nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text='My Claims')
        tree=ttk.Treeview(f,columns=('ID','Item','Type','Status','Note','Date'),show='headings')
        for c in tree['columns']: tree.heading(c,text=c); tree.column(c,width=130)
        tree.pack(fill='both',expand=True)
        def load():
            for x in tree.get_children(): tree.delete(x)
            for r in get_claims(self.user['id']): tree.insert('', 'end', values=(r['id'],r['title'],r['kind'],r['status'],r['note'],r['created']))
        ttk.Button(f,text='Refresh',command=load).pack(pady=8); load()

    def make_mine(self, nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text='My Reports')
        tree=ttk.Treeview(f,columns=('ID','Type','Item','Category','Place','Date','Status'),show='headings')
        for c in tree['columns']: tree.heading(c,text=c); tree.column(c,width=130)
        tree.pack(fill='both',expand=True)
        def load():
            for x in tree.get_children(): tree.delete(x)
            for r in my_items(self.user['id']): tree.insert('', 'end', values=(r['id'],r['kind'],r['title'],r['cat'],r['place'],r['day'],r['status']))
        def done():
            s=tree.selection()
            if not s:return
            iid=tree.item(s[0])['values'][0]
            if close_item(iid,self.user['id']): load(); messagebox.showinfo('Update','Marked as returned.')
        def delete():
            s=tree.selection()
            if not s:return
            iid=tree.item(s[0])['values'][0]
            if messagebox.askyesno('Delete','Delete this report?'): delete_item(iid,self.user['id']); load()
        bar=ttk.Frame(f);bar.pack(fill='x',pady=8)
        ttk.Button(bar,text='Mark returned',command=done).pack(side='left',padx=4)
        ttk.Button(bar,text='Delete report',command=delete).pack(side='left',padx=4)
        ttk.Button(bar,text='Refresh',command=load).pack(side='left',padx=4); load()

    def make_admin(self, nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text='Admin')
        s=stats()
        text='  '.join(f'{k.title()}: {v}' for k,v in s.items())
        ttk.Label(f,text=text,font=('Arial',12,'bold')).pack(pady=8)
        tree=ttk.Treeview(f,columns=('ID','Item','Student','Status','Note'),show='headings')
        for c in tree['columns']: tree.heading(c,text=c); tree.column(c,width=170)
        tree.pack(fill='both',expand=True)
        def load():
            for x in tree.get_children():tree.delete(x)
            for r in get_claims(admin=True):tree.insert('', 'end', values=(r['id'],r['title'],r['student'],r['status'],r['note']))
        def change(st):
            s=tree.selection()
            if not s:return
            cid=tree.item(s[0])['values'][0]
            set_claim(cid,st); load(); messagebox.showinfo('Claim',f'Claim {st}.')
        bar=ttk.Frame(f);bar.pack(pady=8)
        ttk.Button(bar,text='Approve',command=lambda:change('approved')).pack(side='left',padx=4)
        ttk.Button(bar,text='Reject',command=lambda:change('rejected')).pack(side='left',padx=4)
        ttk.Button(bar,text='Refresh',command=load).pack(side='left',padx=4);load()
