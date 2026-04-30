import glob
import json
import mrcfile
import numpy as np

reject = [
'EMD-48782', # emd_48782_msk_1.map range: 0.0000 - 34.8728
'EMD-63643', # "The validation analysis for this entry have not been generated yet."
'EMD-76333', # "The validation analysis for this entry have not been generated yet."
'EMD-72283', # "The validation analysis for this entry have not been generated yet."
'EMD-76334', # "The validation analysis for this entry have not been generated yet"
'EMD-55890', # "The validation analysis for this entry have not been generated yet."
'EMD-65613', # "An unexpected error occurred when attempting to display the validation data for this entry."
'EMD-63947', # emd_63947_msk_1.map is not a mask (range = -0.2242 - 0.4311)
'EMD-63853', # emd_63853_msk_1.map is not a mask (range = -0.3191 - 0.5647)
'EMD-65077', # emd_65077_msk_1.map range: 0.0000 - 26.9748
'EMD-53847', # emd_53847_msk_1.map 1.44 A/px vs reconstruction at 0.72 A/px
'EMD-64391', # Mask voxels all 1.000
'EMD-51161', # "The validation analysis for this entry have not been generated yet."
'EMD-75259', # emd_75259_msk_1.map range: 0.0000 - 0.8821
'EMD-75258', # emd_75258_msk_1.map range: 0.0000 - 0.8889
'EMD-75265', # No FSC validation.
'EMD-52400', # emd_52400_msk_1.map 1 A/px vs reconstruction at 1.4 A/px
]

def volume(map_file, level):
  with mrcfile.open(map_file) as f:
    d = f.data
    if 'msk' in map_file or 'mask' in map_file:
      if d.min() != 0 or d.max() != 1:
        print(f'Warning! {map_file} range: {d.min():0.4f} - {d.max():0.4f}')
    apix = f.voxel_size.x
    summask = (d > level).sum()
    volume = summask*apix**3
    return volume, apix

def calc_vol():
  results = []
  filtered_entries = [e for e in entries if e['id'] not in reject]
  for entry in filtered_entries:
    id = entry['id']
    n = id.split('-')[1]
    if len(glob.glob('emd_%s_msk_*.map.gz' % n)) > 1:
      print(f'Skipping {id} as > 1 masks deposited')
    else:
      map = 'emd_%s.map.gz' % n
      d_mask = 'emd_%s_msk_1.map.gz' % n
      emdb_mask = 'emd_%s.map_mask.mrc.gz' % n
      print(f'Calculating results for {id} using {map}, {d_mask} and {emdb_mask}...')
      map_volume, m_apix = volume(map, entry['recl'])
      d_volume, d_apix = volume(d_mask, 0.5)
      emdb_volume, emdb_apix = volume(emdb_mask, 0.5)
      assert d_apix == emdb_apix
      print(f'...done. Map volume {map_volume:0.2f} Ratio EMDB: {emdb_volume/map_volume:0.2f} Depositor: {d_volume/map_volume:0.2f}')
      results.append({'id':id, 'map_volume':map_volume, 'depositor_mask_volume':d_volume, 'emdb_mask_volume':emdb_volume})

  for r in sorted(results, key=lambda x: x['emdb_mask_volume']/x['depositor_mask_volume']):
    print(f'{r['id']} ratio:{r['emdb_mask_volume']/r['depositor_mask_volume']:0.2f}')
  with open('results_2026-04-27.json', 'w') as f:
    json.dump(results, f)

if __name__ == '__main__':
  with open('entries_2026-04-27.json') as f:
    entries = json.load(f)
  calc_vol()