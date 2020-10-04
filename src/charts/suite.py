import os

PENETRATION = [.01, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99]
N = 1
STEPS = 10000
SKIP = 1000

for p in PENETRATION:
    penetration = int(p * 100)
    prefix = f'p{penetration:02d}'
    for i in range(N):
        os.system(f'python src/main.py --penetration {p} --length 100 --lanes 3'
                  f' --obstacles=1:50-50 --symmetry cli --steps {STEPS} --skip {SKIP}'
                  f' --output=out --prefix="{prefix}__{i:02d}" --no-charts --travel --heatmap')
    os.system(f'python src/charts/heatmap.py'
              f' -o out -p {prefix}.traffic -s 5 out/{prefix}__*_traffic.csv')
    os.system(f'python src/charts/travel.py -o out -p {prefix}.travel'
              f' out/{prefix}__*_travel.csv')
    os.system(f'python src/charts/average.py -o out -p {prefix}.average'
              f' -x {penetration} out/{prefix}__*_average.csv')

os.system('python src/charts/average.py --output=out --prefix=average out/*.average.csv')
os.system('python src/charts/penetration.py --output=out --prefix=average out/average.csv')
