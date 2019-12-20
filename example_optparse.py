import optparse

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option("-b","--batch",   dest="runBatch", help="Run in batch"                              , default=False  , action="store_true")

(options, args) = parser.parse_args()

print options.runBatch
