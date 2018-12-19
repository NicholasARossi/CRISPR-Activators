from os import listdir
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np



def main():
    ### This is the driver for visulaizing all the experiments, each strain includes cells from 15 xy positioins collected
    # over 3 days (5 positions each day)
    # Glucose --> Arabinose Experiments are the first row
    # Glucose --> Gluocose Experiments are the second row

    plt.close('all')
    fig, ax = plt.subplots(2, 5, sharey=True, sharex=True, figsize=(20, 8))

    folders = ['104_arabinose', '105_arabinose', '108_arabinose', '109_arabinose', '112_arabinose', '104_glucose',
               '105_glucose', '108_glucose', '109_glucose', '112_glucose']

    # Color edits
    colorz = ["#00a6ca", "#00ccbc", "#90eb9d", "#f9d057", "#f29e2e", "#e76818", "#d7191c"];

    glucose_limit = 20
    for n, folder in enumerate(folders):
        z = 0
        names = listdir(folder)

        if '.DS_Store' in names:
            names.remove('.DS_Store')
        names = sorted(names, key=lambda x: int(x.split('_')[1]))

        for name in names:
            if z == 0:
                temp_data = np.empty((1, glucose_limit,))
                temp_data[:] = np.nan

            mat_contents = sio.loadmat(folder + '/' + name)

            temp_data = np.vstack((temp_data, mat_contents['data3D'][:, 5][:, 0:glucose_limit]))
            z += 1

        y = np.nanmean(temp_data, 0)
        error = np.nanstd(temp_data, 0)
        t_vect = np.linspace(0, 10 * (glucose_limit - 1), glucose_limit)
        ax[int(np.floor(n / 5)), n % 5].fill_between(t_vect, y - error, y + error, color='#d3d3d3', alpha=1)
        ax[int(np.floor(n / 5)), n % 5].plot(t_vect, y, color=colorz[n % 5])
        ax[int(np.floor(n / 5)), n % 5].set_title(folder)
        ax[int(np.floor(n / 5)), n % 5].set_xlabel('Time (Minutes)')
    ax[0, 0].set_ylabel('GFP (A.U.)')
    ax[1, 0].set_ylabel('GFP (A.U.)')

    fig.savefig('figures/arabinose.png', dpi=300)
if __name__ == "__main__":
    print("Generating Graphs for Glucose vs Arabinose")
    main()