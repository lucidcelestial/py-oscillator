from soundio import IO

BLOCK_SIZE = 8
SAMPLE_RATE = 44100

# make a new IO instance with a given sample block size and sample rate
io = IO(BLOCK_SIZE, SAMPLE_RATE)
