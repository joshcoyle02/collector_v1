# netcool-collector
Read-only collector that extracts IBM Netcool/OMNIbus configuration and event data from a client estate to inform a migration off it.

# How it works
Run the "collector.py" file.  This calls the run_extraction function which has all four extraction methods in it.
Fill in the parameters on collector.py for the instance.

# 29/06/2026

Through the testing scripts I have documented that the collector modules do work.
Next step is to test it on a AWS instance with the collector.py parameters populated.