The isis2json.py is a Jython script to export ISIS databases to JSON files.

isis2json.py depends on:

- Jython 2.5;
- zeusIII.jar on the CLASSPATH;
- jyson-1.0.1.jar on the CLASSPATH;
- argparse.py on the current directory or the PYTHONPATH (*);

Example CLASSPATH:

export CLASSPATH=/home/luciano/lib/zeusIII.jar:/home/luciano/lib/jyson-1.0.1.jar

(*) The argparse module is part of the CPython 2.7 distribution

