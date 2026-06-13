import numpy as np
import sys
from roller_core import compute

D         = 8e-3
L         = 50e-3
h_target  = 150e-6
sigma_A   = 200 / 1000
D50       = 15e-6
h0        = 356e-6
sigma_y   = 50e6

print('=' * 60)
print('  Roller Compaction Parametric Study')
print('=' * 60)
print(f'  Roller D     = {D*1e3:.0f} mm')
print(f'  Roller L     = {L*1e3:.0f} mm')
print(f'  Feed h0      = {h0*1e6:.0f} um')
print(f'  Gap h        = {h_target*1e6:.0f} um')
print(f'  Areal mass   = {sigma_A*1e3:.0f} g/m2')
print(f'  D50          = {D50*1e6:.0f} um')
print(f'  sigma_y      = {sigma_y/1e6:.0f} MPa')
print(f'  Feed R0      = {sigma_A/(2250*h0):.3f}')
print(f'  Target R     = {sigma_A/(2250*h_target):.3f}')
print()

S, F_tot, d_bend, d_cont, pm, _, _, _, _ = compute(D, L, h_target, h0, sigma_y, sigma_A)

print(f'  S={S*1e3:.2f}mm  pmax={pm/1e6:.3f}MPa  F={F_tot:.1f}N  dbend={d_bend*1e6:.2f}um  dcont={d_cont*1e6:.2f}um')
print()
print(f'  --- Results ---')
print(f'  Contact arc   = {S*1e3:.2f} mm')
print(f'  Total force   = {F_tot:.1f} N')
print(f'  Bend defl     = {d_bend*1e6:.2f} um')
print(f'  Contact defl  = {d_cont*1e6:.2f} um')
print(f'  Gap deviation = {d_bend/h_target*100:.2f}%')
print(f'  Mid-gap       = {(h_target+d_bend)*1e6:.1f} um')
dev = d_bend/h_target * 100
grade = 'A: negligible' if dev<1 else 'B: marginal' if dev<5 else 'C: significant' if dev<10 else 'D: unacceptable'
print(f'  Grade         = {grade}')
print('=' * 60)

if '--sweep' in sys.argv:
    print()
    print('=' * 60)
    print('  Parametric Sweeps')
    print('=' * 60)
    print()
    print('[Sweep 1] Roller length L (mm)')
    for Lv in [10,15,20,25,30,35,40,45,50,60,70,80,90,100]:
        s, f, d, _, _, _, _, _, _ = compute(D, Lv*1e-3, h_target, h0, sigma_y, sigma_A)
        dv = d/h_target*100
        g = 'A' if dv<1 else 'B' if dv<5 else 'C' if dv<10 else 'D'
        print(f'  {Lv:8.0f}  {d*1e6:8.2f}  {dv:8.2f}  {f:8.2f}  {s*1e3:8.2f}  {g:>6s}')
    print()
    print('[Sweep 2] Roller diameter D (mm)')
    for Dv in [4,6,8,10,12,14,16,18,20,25,30,40,50,60,80,100]:
        s, f, d, _, _, _, _, _, _ = compute(Dv*1e-3, L, h_target, h0, sigma_y, sigma_A)
        dv = d/h_target*100
        g = 'A' if dv<1 else 'B' if dv<5 else 'C' if dv<10 else 'D'
        print(f'  {Dv:8.0f}  {s*1e3:8.2f}  {d*1e6:8.2f}  {dv:8.2f}  {f:8.2f}  {g:>6s}')
    print()
    print('[Sweep 3] Feed thickness h0 (um)')
    for h0v in [200,250,300,350,400,450,500,550,600,650,700,750,800]:
        s, f, d, _, _, _, _, _, _ = compute(D, L, h_target, h0v*1e-6, sigma_y, sigma_A)
        print(f'  {h0v:8.0f}  {s*1e3:8.2f}  {d*1e6:8.2f}  {d/h_target*100:8.2f}  {f:8.2f}')
    print()
    print('[Sweep 4] Target gap h (um)')
    for hv in [50,80,100,120,150,180,200,250,300]:
        s, f, d, _, _, _, _, _, _ = compute(D, L, hv*1e-6, h0, sigma_y, sigma_A)
        r = sigma_A/(2250*hv*1e-6)
        print(f'  {hv:8.0f}  {r:8.3f}  {d*1e6:8.2f}  {d/hv*1e-2:8.2f}  {f:8.2f}')
    print()
    print('[Sweep 5] Effective yield sigma_y (MPa)')
    for syv in [10,20,30,40,50,60,80,100,150,200]:
        s, f, d, _, pm_val, _, _, _, _ = compute(D, L, h_target, h0, syv*1e6, sigma_A)
        print(f'  {syv:8.0f}  {pm_val/1e6:10.2f}  {d*1e6:8.2f}  {d/h_target*100:8.2f}  {f:8.2f}')
    print()
    print('=' * 60)

if '--help' in sys.argv:
    print('Roller Compaction Parametric Study')
    print('python roller_study.py / --sweep / --help')
