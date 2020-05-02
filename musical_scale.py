import pandas as pd

df = pd.DataFrame({'Note': ['C'], 'Octave': [4], 'Frequency': [261.63]},
                  columns=['Note', 'Octave', 'Frequency'])

notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

def looper(index, increment):
    # This function simply returns the index back
    # to zero if it exceeds the length of 'notes'.
    if index + increment > 6:
        return index + increment - 7
    else:
        return index + increment


def make_octaves(note, octave):
    # Extract row that matches note and octave
    row = df.loc[(df['Note'] == note) & (df['Octave'] == octave)]
    print(row)
    # Generate all octaves of that note
    # skipping the one that already exists
    for i in [x for x in range(9) if x != octave]:
        # Every octave of a note is double the frequency
        # of the previous octave
        df.loc[len(df)] = [row.iloc[0]['Note'],
                           row.iloc[0]['Octave'] + (i - octave),
                           (2.**(i - octave))*row.iloc[0]['Frequency']]

def make_fifth(note, octave):
    # Extract row that matches note and octave
    row = df.loc[(df['Note'] == note) & (df['Octave'] == octave)]
    if notes.index(row.iloc[0]['Note']) + 4 > 6:
        new_note_idx = notes.index(row.iloc[0]['Note']) + 4 - 7
        octave_inc = 1
    else:
        new_note_idx = notes.index(row.iloc[0]['Note']) + 4
        octave_inc = 0
    # 3 half-wavelengths fit between the two nodes
    # of any resonator to make a 'fifth'. Therefore
    # we multiply the root note frequency by 1.5 to
    # get the fifth's frequency
    new_note = [notes[new_note_idx],
                       row.iloc[0]['Octave'] + octave_inc,
                       1.5 * row.iloc[0]['Frequency']]
    df.loc[len(df)] = new_note
    return new_note

curr_note = 'C'
curr_oct = 4
while len(df.index) < 63:
    make_octaves(curr_note, curr_oct)
    new_line = make_fifth(curr_note, 4)
    curr_note = new_line[0]
    curr_oct = new_line[1]
    print(new_line)

df.sort_values(by=['Octave', 'Note'],inplace=True)
df.to_csv(r'data/processed/scale.csv', index=False)
print(df)