import pickle as pkl


def load_data(save_path='Data/Unified_ratings.pkl'):
    with open(save_path, 'rb') as f:
        df = pkl.load(f)
    return df


if __name__=='__main__':
    # Test that loader works
    df = load_data()
    print(df.shape)