import json
import matplotlib.pyplot as plt

def plot():
  with open('results_2026-04-27.json') as f:
    results = json.load(f)
  for r in sorted(results, key=lambda x: x['emdb_mask_volume']/x['depositor_mask_volume']):
    print(f'{r['id']} ratio:{r['emdb_mask_volume']/r['depositor_mask_volume']:0.2f}')
  x = [r['emdb_mask_volume']/r['map_volume'] for r in results]
  y = [r['depositor_mask_volume']/r['map_volume'] for r in results]
  for d, mask in [[x,'EMDB'], [y, 'Depositor']]:
    fig, ax = plt.subplots()
    ax.hist(d, bins=100, range=(0,200))
    ax.set_xlim(0,200)
    ax.set_xlabel(f'Volume ratio {mask} mask:Primary map')
    ax.set_ylabel('Count')
    plt.title(f'{mask} mask volume compared to Primary map volume')
    fig.savefig(f'results_{mask}_2026-04-27.pdf', format='pdf')

if __name__ == '__main__':
  plot()
