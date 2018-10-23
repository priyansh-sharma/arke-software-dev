import boto3

STREAM_NAME = "priyansh"
kvs = boto3.client("kinesisvideo")
# Grab the endpoint from GetDataEndpoint
endpoint = kvs.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamName=STREAM_NAME
)['DataEndpoint']
# Grab the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
url = kvam.get_hls_streaming_session_url(
    StreamName=STREAM_NAME,
    PlaybackMode="LIVE"
)['HLSStreamingSessionURL']

print(url)
print(url == "https://b-604520a7.kinesisvideo.us-east-1.amazonaws.com/hls/v1/getHLSMasterPlaylist.m3u8?SessionToken=CiAmPm41kyf4Z4ITJ9cmMiV1m5H6lmfHycwgiTvt9KEl4xIQUtGEt_KU97rO5Znm0P_MdxoZflv9zdzbYjVFDvi3X3mJxhDFNlxzQ6iGOiIgADA2zdtrxWui6NiHsClVjlfCcxKJAdCGyShBZJ6P1Qc~")