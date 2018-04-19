from optparse import OptionParser
import ConfigParser
import os

def get_config(conf, section, key):
    if os.path.exists(conf):
        value = ""
        config = ConfigParser.ConfigParser()
        config.read(conf)
        try:
            value = config.get(section, key)
            print ("{}={}".format(key, value))
        except Exception, e:
            print e
    else:
        print ("can't find path: {}".format(conf))

def main():
    usage = "usage: python %prog [options]\n    OR ./%prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", action="store_true", dest="read")
    parser.add_option("-w", action="store_true", dest="write")
    parser.add_option("-f", "--file", type="string", action="store", dest="file")
    parser.add_option("-s", "--section", type="string", action="store", dest="section")
    parser.add_option("-k", "--key", type="string", action="store", dest="key")
    (options, args) = parser.parse_args()

    if options.read:
        get_config(options.file, options.section, options.key)

if __name__ == "__main__":
    main()