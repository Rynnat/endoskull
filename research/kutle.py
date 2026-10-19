import math
g=9.81
# (ad, gram, x_mm ileri, z_mm yukari, k_mm kendi jirasyon yaricapi)  pivot P2 = orijin
base=[("kafatasi kubbe+arka",280,-5,95,55),("yuz (kas,elmacik,ust dis)",150,65,55,35),
("cene (mandibula)",90,50,-20,30),("boyun ust plaka/U-mafsal kafa yarisi",40,0,5,20),
("goz baskili (2 kure,3 kapak,cerceve,link)",55,70,70,15),("5x SG90",45,40,70,10),
("cene MG996R + kol",60,20,25,15),("PCA9685",10,0,60,10),("vida+somun",50,20,50,40),
("kablo+LED",25,15,50,30),("ball-link/pushrod uclari",5,40,0,5)]
L1=[("kafatasi kubbe+arka",120,-5,95,55),("yuz",80,65,55,35),("cene",45,50,-20,30),
("sahte detay (civata basi,oluk,piston kilifi)",15,30,60,40),("boyun ust plaka",30,0,5,20),
("goz baskili",40,70,70,15),("5x SG90",45,40,70,10),("cene MG996R + kol",60,20,25,15),
("PCA9685",10,0,60,10),("vida+somun",25,20,50,40),("kablo+LED",15,15,50,30),("ball-link",5,40,0,5)]
def mv(lst,name,**kw):
    out=[]
    for t in lst:
        if t[0].startswith(name):
            t=list(t)
            for k,v in kw.items(): t[{"m":1,"x":2,"z":3}[k]]=v
            t=tuple(t)
        out.append(t)
    return out
L2=mv(L1,"5x SG90",x=15,z=15); L2=mv(L2,"cene MG996R",x=-10,z=0); L2=mv(L2,"PCA",x=-45,z=35)
L2=L2+[("uzun goz cubuklari (4x1mm celik ~70mm)",3,45,40,5)]
L3=[t for t in L2 if not t[0].startswith("cene MG996R")]+[("Bowden kilif ucu+kablo (kafa tarafi)",8,10,0,10)]
def calc(lst,th):
    m=sum(t[1] for t in lst)/1000
    Mx=sum(t[1]*t[2] for t in lst)/1000; Mz=sum(t[1]*t[3] for t in lst)/1000
    x=Mx/m; z=Mz/m
    I=sum(t[1]/1000*((t[2]**2+t[3]**2)+t[4]**2) for t in lst)*1e-6
    a=8.4
    st=m*(x*math.cos(math.radians(th))+z*math.sin(math.radians(th)))/10  # kg*cm (mm->cm)
    dyn=I*a/g*100
    return m,x,z,I,st,dyn
for name,lst in [("BAZ (S1 naif)",base),("L1 ince kabuk",L1),("L2 L1+servolar tabana",L2),("L3 L2+cene servosu govdede",L3)]:
    print("==",name)
    for th in (30,-30):
        m,x,z,I,st,dyn=calc(lst,th)
        tot=abs(st)+dyn
        print(f" th={th:+d} m={m*1000:.0f}g CG=({x:.1f},{z:.1f}) L={math.hypot(x,z):.1f} I={I*1e4:.1f}e-4 stat={st:.2f} dyn={dyn:.2f} TOT={tot:.2f} | pay C1 {3.5/tot:.2f} C2 {7/tot:.2f} C3 {14/tot:.2f} | x1.3 kutle C3 {14/(tot*1.3):.2f} C2 {7/(tot*1.3):.2f}")
# yay: L2 at +30 -> spring cancels 50%/70% of static
# Euler burkulma 1mm celik
E=200e9; d=1e-3; I=math.pi*d**4/64
for Lr in (0.06,0.1): print("burkulma",Lr, math.pi**2*E*I/Lr**2)
# kaburga esdeger
def plateI(t,w=20): return w*t**3/12
def TI(t=1.2,rb=1.6,h=5,w=20):
    A1=w*t; y1=t/2; A2=rb*h; y2=t+h/2
    yc=(A1*y1+A2*y2)/(A1+A2)
    return w*t**3/12+A1*(y1-yc)**2+rb*h**3/12+A2*(y2-yc)**2, A1+A2
Ir,Ar=TI()
teq=(Ir*12/20)**(1/3)
print("kaburgali I",Ir,"alan",Ar,"esdeger t",teq,"kutle orani vs esdeger",Ar/(20*teq), "vs 2.5mm", Ar/(20*2.5), "I vs 2.5", Ir/plateI(2.5))
# kabuk alani
a,b,c=100,77.5,115;p=1.6
S=4*math.pi*(((a*b)**p+(a*c)**p+(b*c)**p)/3)**(1/p)
print("elipsoid alan cm2",S/100, "1.2mm PLA g", S*1.2/1000*1.24, "2.5mm", S*2.5/1000*1.24)
# vida kutleleri celik
rho=7.85e-3
def vida(d,L,hd,hh): return (math.pi*(d/2)**2*L+math.pi*(hd/2)**2*hh)*rho
def somun(s,m,d): return (s*s*math.sqrt(3)/2 - math.pi*(d/2)**2)*m*rho
print("M3x14+somun",vida(3,14,5.5,2)+somun(5.5,2.4,3),"M3x8+s",vida(3,8,5.5,2)+somun(5.5,2.4,3),"M2x8+s",vida(2,8,3.8,1.4)+somun(4,1.6,2))
# cene dusme suresi
Ij=3.6e-4; tau=0.09*g*0.05*math.cos(math.radians(20)); al=tau/Ij; print("cene dusme 20deg s",math.sqrt(2*math.radians(20)/al))
print("== marjinal (L1'den, +30 toplam)")
def tot(l): m,x,z,I,st,dyn=calc(l,30); return st+dyn
t0=tot(L1)
cases={"SG90'lar tabana":mv(L1,"5x SG90",x=15,z=15),
"cene servo pivot arkasi":mv(L1,"cene MG996R",x=-10,z=0),
"cene servo govdeye(Bowden)":[t for t in L1 if not t[0].startswith("cene MG996R")]+[("bowden",8,10,0,10)],
"PCA arkaya":mv(L1,"PCA",x=-45,z=35),
"PCA govdeye":[t for t in L1 if not t[0].startswith("PCA")]}
for k,v in cases.items(): print(f" {k}: {tot(v)-t0:+.2f} kg*cm")
# yaw ataleti kaba: m*(k^2) ile
for n,l in [("BAZ",base),("L2",L2)]:
    Iy=sum(t[1]/1000*((t[2]-20)**2+(t[4])**2+ 40**2) for t in l)*1e-6
    print(n,"yaw I~",Iy)
