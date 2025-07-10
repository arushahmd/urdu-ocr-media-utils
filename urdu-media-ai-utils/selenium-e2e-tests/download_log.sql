-- Drop the table if it exists
DROP TABLE IF EXISTS job_manager_downloadlog;

-- Create the table with item_id as the primary key
CREATE TABLE job_manager_downloadlog (
    item_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    batch_id INT NOT NULL,  -- Allow null values for batch_id
    url VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT NULL,
    status VARCHAR(50) NOT NULL,
    duration INT NOT NULL,  -- Duration in milliseconds
    date DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Current timestamp when a record is created
    download_duration INT NOT NULL,  -- Download duration in milliseconds
    error_message VARCHAR(255) DEFAULT NULL
);

-- Insert the records with appropriate milliseconds for duration and download_duration
INSERT INTO job_manager_downloadlog (item_id, user_id, batch_id, url, title, status, duration, download_duration, error_message)
VALUES
(1, 233, 1, 'https://youtu.be/example1', 'Sample Video 1', 'Completed', 3476000, 98000, 'Downloading succeeded'),
(2, 233, 1, 'https://youtu.be/example2', 'Sample Video 2', 'Stopped', 2783000, 98000, 'Job with same link already exists'),
(3, 233, 1, 'https://youtu.be/example3', '', 'Failed', 3224000, 307000, 'Failed due to network issues'),
(4, 3, 2, 'https://youtu.be/example4', 'Negotiations of Govt and PTI', 'Completed', 3224000, 210000, 'Downloading succeeded'),
(5, 20, 3, 'https://youtu.be/example5', '', 'Failed', 3224000, 3224000, 'Downloading failed with pytube'),
(6, 233, 3, 'https://youtu.be/example6', 'Sample Video 3', 'Completed', 3599000, 150000, 'Downloading succeeded'),
(7, 3, 3, 'https://youtu.be/example7', '', 'Failed', 2730000, 255000, 'Failed due to throttling issues'),
(8, 20, 4, 'https://youtu.be/example8', 'Sample Video 4', 'Completed', 2950000, 120000, 'Downloading succeeded'),
(9, 233, 4, 'https://youtu.be/example9', 'Sample Video 5', 'Stopped', 3130000, 2950000, 'Job with same link already exists'),
(10, 3, 5, 'https://youtu.be/example10', '', 'Failed', 3030000, 3315000, 'Failed due to network issues'),
(11, 20, 5, 'https://youtu.be/example11', 'Sample Video 6', 'Completed', 3315000, 105000, 'Downloading succeeded'),
(12, 233, 6, 'https://youtu.be/example12', '', 'Failed', 3480000, 105000, 'Failed due to throttling issues'),
(13, 3, 6, 'https://youtu.be/example13', 'Sample Video 7', 'Completed', 2720000, 195000, 'Downloading succeeded'),
(14, 20, 7, 'https://youtu.be/example14', 'Sample Video 8', 'Stopped', 2820000, 150000, 'Job with same link already exists'),
(15, 233, 7, 'https://youtu.be/example15', '', 'Failed', 3010000, 245000, 'Failed due to network issues'),
(16, 3, 8, 'https://youtu.be/example16', 'Sample Video 9', 'Completed', 2925000, 150000, 'Downloading succeeded'),
(17, 20, 8, 'https://youtu.be/example17', '', 'Failed', 3085000, 150000, 'Downloading failed with pytube'),
(18, 233, 9, 'https://youtu.be/example18', 'Sample Video 10', 'Completed', 2640000, 70000, 'Downloading succeeded'),
(19, 3, 9, 'https://youtu.be/example19', '', 'Failed', 2955000, 300000, 'Failed due to throttling issues'),
(20, 20, 10, 'https://youtu.be/example20', 'Sample Video 11', 'Stopped', 2790000, 3135000, 'Job with same link already exists'),
(21, 233, 10, 'https://youtu.be/example21', '', 'Failed', 2740000, 230000, 'Failed due to network issues'),
(22, 3, 11, 'https://youtu.be/example22', 'Sample Video 12', 'Completed', 2875000, 135000, 'Downloading succeeded'),
(23, 20, 11, 'https://youtu.be/example23', '', 'Failed', 3135000, 2790000, 'Downloading failed with pytube'),
(24, 233, 12, 'https://youtu.be/example24', 'Sample Video 13', 'Completed', 3510000, 115000, 'Downloading succeeded'),
(25, 3, 12, 'https://youtu.be/example25', '', 'Failed', 3240000, 3510000, 'Failed due to throttling issues'),
(26, 20, 13, 'https://youtu.be/example26', 'Sample Video 14', 'Stopped', 2950000, 2790000, 'Job with same link already exists'),
(27, 233, 13, 'https://youtu.be/example27', '', 'Failed', 3200000, 270000, 'Failed due to network issues');




-- Create the table
CREATE TABLE job_manager_downloadlog (
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    batch_id INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT NULL,
    status VARCHAR(50) NOT NULL,
    duration VARCHAR(20) DEFAULT NULL,
    size VARCHAR(20) DEFAULT NULL,
    download_duration VARCHAR(20) DEFAULT NULL,
    attempts INT DEFAULT 1,
    error_message TEXT DEFAULT NULL
);



INSERT INTO job_manager_downloadlog (user_id, job_id, batch_id, url, title, status, duration, size, download_duration, attempts, error_message)
VALUES
(233, 101, 1, 'https://youtu.be/example1', 'Sample Video 1', 'Completed', '0:57:56', 'N/A', '0:01:38', 1, 'Downloading succeeded'),
(233, 102, 1, 'https://youtu.be/example2', 'Sample Video 2', 'Stopped', '0:46:23', 'N/A', NULL, 1, 'Job with same link already exists'),
(233, 103, 1, 'https://youtu.be/example3', '', 'Failed', '0:53:44', 'N/A', '0:05:07', 1, 'Failed due to network issues'),
(3, 104, 2, 'https://youtu.be/example4', 'Negotiations of Govt and PTI', 'Completed', '0:53:44', 'N/A', '0:03:30', 1, 'Downloading succeeded'),
(20, 105, 3, 'https://youtu.be/example5', '', 'Failed', '0:53:44', 'N/A', NULL, 1, 'Downloading failed with pytube'),
(233, 106, 3, 'https://youtu.be/example6', 'Sample Video 3', 'Completed', '0:59:59', 'N/A', '0:02:30', 1, 'Downloading succeeded'),
(3, 107, 3, 'https://youtu.be/example7', '', 'Failed', '0:45:30', 'N/A', '0:04:15', 1, 'Failed due to throttling issues'),
(20, 108, 4, 'https://youtu.be/example8', 'Sample Video 4', 'Completed', '0:49:20', 'N/A', '0:02:00', 1, 'Downloading succeeded'),
(233, 109, 4, 'https://youtu.be/example9', 'Sample Video 5', 'Stopped', '0:52:10', 'N/A', NULL, 1, 'Job with same link already exists'),
(3, 110, 5, 'https://youtu.be/example10', '', 'Failed', '0:50:30', 'N/A', NULL, 1, 'Failed due to network issues'),
(20, 111, 5, 'https://youtu.be/example11', 'Sample Video 6', 'Completed', '0:55:15', 'N/A', '0:01:45', 1, 'Downloading succeeded'),
(233, 112, 6, 'https://youtu.be/example12', '', 'Failed', '0:58:00', 'N/A', NULL, 1, 'Failed due to throttling issues'),
(3, 113, 6, 'https://youtu.be/example13', 'Sample Video 7', 'Completed', '0:45:20', 'N/A', '0:03:15', 1, 'Downloading succeeded'),
(20, 114, 7, 'https://youtu.be/example14', 'Sample Video 8', 'Stopped', '0:47:00', 'N/A', NULL, 1, 'Job with same link already exists'),
(233, 115, 7, 'https://youtu.be/example15', '', 'Failed', '0:50:10', 'N/A', '0:04:05', 1, 'Failed due to network issues'),
(3, 116, 8, 'https://youtu.be/example16', 'Sample Video 9', 'Completed', '0:48:45', 'N/A', '0:02:30', 1, 'Downloading succeeded'),
(20, 117, 8, 'https://youtu.be/example17', '', 'Failed', '0:51:25', 'N/A', NULL, 1, 'Downloading failed with pytube'),
(233, 118, 9, 'https://youtu.be/example18', 'Sample Video 10', 'Completed', '0:44:00', 'N/A', '0:01:10', 1, 'Downloading succeeded'),
(3, 119, 9, 'https://youtu.be/example19', '', 'Failed', '0:49:15', 'N/A', '0:05:00', 1, 'Failed due to throttling issues'),
(20, 120, 10, 'https://youtu.be/example20', 'Sample Video 11', 'Stopped', '0:46:30', 'N/A', NULL, 1, 'Job with same link already exists'),
(233, 121, 10, 'https://youtu.be/example21', '', 'Failed', '0:45:40', 'N/A', '0:03:50', 1, 'Failed due to network issues'),
(3, 122, 11, 'https://youtu.be/example22', 'Sample Video 12', 'Completed', '0:47:55', 'N/A', '0:02:15', 1, 'Downloading succeeded'),
(20, 123, 11, 'https://youtu.be/example23', '', 'Failed', '0:52:15', 'N/A', NULL, 1, 'Downloading failed with pytube'),
(233, 124, 12, 'https://youtu.be/example24', 'Sample Video 13', 'Completed', '0:58:30', 'N/A', '0:01:55', 1, 'Downloading succeeded'),
(3, 125, 12, 'https://youtu.be/example25', '', 'Failed', '0:54:00', 'N/A', NULL, 1, 'Failed due to throttling issues'),
(20, 126, 13, 'https://youtu.be/example26', 'Sample Video 14', 'Stopped', '0:49:10', 'N/A', NULL, 1, 'Job with same link already exists'),
(233, 127, 13, 'https://youtu.be/example27', '', 'Failed', '0:53:20', 'N/A', '0:04:30', 1, 'Failed due to network issues');


#### Replace '' title with Title not Available, 

UPDATE job_manager_downloadlog
SET title = 'Title not available'
WHERE title = '';








