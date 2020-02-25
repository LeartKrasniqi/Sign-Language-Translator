from google.cloud import storage
import time

client = storage.Client()

bucket = client.bucket('slab-asl-testing')

testBlob = bucket.blob('test_blob')
time1 = time.time()
testBlob.upload_from_filename(filename='./' + 'video0.h264')
time2 = time.time()
print("Seconds: ",  time2 - time1)
