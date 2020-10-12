import logging
from jarvis.core.processor import Processor


def main():
    processor = Processor()
    
    while True:
        processor.run()
    
main()