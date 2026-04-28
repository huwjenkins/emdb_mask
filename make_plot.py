import json
import seaborn as sns
import matplotlib.pyplot as plt

def plot():
  with open('results_2026-04-27.json') as f:
    results = json.load(f)
  for r in sorted(results, key=lambda x: x['emdb_mask_volume']/x['depositor_mask_volume']):
    print(f'{r['id']} ratio:{r['emdb_mask_volume']/r['depositor_mask_volume']:0.2f}')
  a = [r['emdb_mask_volume']/r['depositor_mask_volume'] for r in results]
  fig, ax = plt.subplots()
  sns.stripplot(data=a, orient='h', size=4, jitter=0.25)
  ax.xaxis.grid(which='both')
  ax.set_xlabel('Volume ratio EMDB mask:Depositors mask')
  ax.set_xlim(0,50)
  ax.xaxis.set_ticks(range(0,51,5))
  fig.savefig('results_2026-04-27.pdf', format='pdf')
  ax.set_xlim(0,20)
  ax.xaxis.set_ticks(range(0,21,1))
  fig.savefig('results_2026-04-27_zoom.pdf', format='pdf')
if __name__ == '__main__':
  plot()
