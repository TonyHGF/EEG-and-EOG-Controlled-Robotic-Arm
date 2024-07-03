from openbci_stream.acquisition import Cyton


openbci = Cyton('serial', endpoint='/dev/ttyUSB0', capture_stream=True)

# blocking call
openbci.stream(15)  # collect data for 15 seconds