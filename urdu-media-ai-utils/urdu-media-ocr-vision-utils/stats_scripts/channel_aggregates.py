import csv
from ArooshScripts.utils.common import count_files_in_channels, channels


def print_channel_stats(header, channel_counts, total_unique_channels, total_top, total_middle, total_bottom):
    print(header)

    # Print the results for each channel
    for channel, counts in channel_counts.items():
        print(f'{channel}: {counts["low"]} Low, {counts["above"]} Above, {counts["middle"]} Middle'
              f', Total: {counts["low"] + counts["above"] + counts["middle"]}, Total_Images {counts["images"]}')

    print(f'Total Unique Channels: {total_unique_channels}')
    print(f'Total Instances: {sum(counts["total"] for counts in channel_counts.values())}')
    print(f'Total Top Annotations: {total_top}')
    print(f'Total Middle Annotations: {total_middle}')
    print(f'Total Bottom Annotations: {total_bottom}\n')


def write_to_csv(csv_path, channel_counts, set_type):
    with open(csv_path, mode='w', newline='') as csv_file:
        fieldnames = ['Channel', 'Low', 'Above', 'Middle', 'Total', 'Total_Images', 'Set_Type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        # Writing stats to CSV
        for channel, counts in channel_counts.items():
            writer.writerow({
                'Channel': channel,
                'Low': counts['low'],
                'Above': counts['above'],
                'Middle': counts['middle'],
                'Total': counts['low'] + counts['above'] + counts['middle'],
                'Total_Images': counts['images'],
                'Set_Type': set_type
            })


if __name__ == "__main__":
    train_annotations_dir = '/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/NewDataset/BalancedData/Train/annotations_urdu'
    train_images_dir = '/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/NewDataset/BalancedData/Train/images'
    test_annotations_dir = '/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/NewDataset/BalancedData/Test/annotations_urdu'
    test_images_dir = '/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/NewDataset/BalancedData/Test/images'

    # Training set stats
    train_channel_counts, train_total_unique_channels, train_total_top, train_total_middle, train_total_bottom = count_files_in_channels(
        train_annotations_dir, channels, train_images_dir)
    print_channel_stats("Training BioData:", train_channel_counts, train_total_unique_channels, train_total_top,
                        train_total_middle, train_total_bottom)

    # Testing set stats
    test_channel_counts, test_total_unique_channels, test_total_top, test_total_middle, test_total_bottom = count_files_in_channels(
        test_annotations_dir, channels, test_images_dir)
    print_channel_stats("Testing BioData:", test_channel_counts, test_total_unique_channels, test_total_top,
                        test_total_middle, test_total_bottom)

    csv_train_path = ('/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts'
                      '/6. statistics/channel_stats_train_exp_bal.csv')
    csv_test_path = ('/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts/6. statistics'
                     '/channel_stats_test_exp_bal.csv')
    csv_total_path = ('/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts'
                      '/6. statistics/channel_stats_total_exp_bal.csv')

    # Writing stats to CSV for training set
    write_to_csv(csv_train_path, train_channel_counts, 'Train')

    # Writing stats to CSV for testing set
    write_to_csv(csv_test_path, test_channel_counts, 'Test')

    # Writing total stats to CSV
    total_channel_counts = {channel: {'low': counts['low'] + test_channel_counts[channel]['low'],
                                      'above': counts['above'] + test_channel_counts[channel]['above'],
                                      'middle': counts['middle'] + test_channel_counts[channel]['middle'],
                                      'images': counts['images'] + test_channel_counts[channel]['images'],
                                      'total': counts['total'] + test_channel_counts[channel]['total']}
                            for channel, counts in train_channel_counts.items()}

    write_to_csv(csv_total_path, total_channel_counts, 'Total')
