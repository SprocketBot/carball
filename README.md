# Sprocket-carball
Sprocket-carball is an open-source project that combines multiple tools for
decompiling Rocket League replays and then analysing them. It is a fork of
[SaltieRL's carball](https://github.com/SaltieRL/carball) project, which 
appears to no longer be maintained. 

## Requirements

- Python 3.6.7+ (3.7 and 3.8 included)
- Windows, Mac or Linux

## Install

#### Install from pip:

`pip install sprocket_carball`

#### Clone for development

##### Windows
```
git clone https://github.com/SprocketBot/carball
cd carball/
python init.py
```

##### Linux
```
git clone https://github.com/SprocketBot/carball
cd carball/
./_travis/install-protoc.sh
python init.py
```

Alternatively, 

```
git clone https://github.com/SprocketBot/carball
cd carball/
./utils/install_protobuf.sh
python init.py
sudo python setup.py install
```

Finally, to publish the package on PyPI

```
python setup.py sdist
twine upload dist/*
```

To actually *use* the package as writ (until we get the protobuf version that we
use for generating the pb2 files updated), you'll need to set this environment
variable:

```
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```


##### Mac
In MacOS Catalina, zsh replaced bash as the default shell, which may cause permission issues when trying to run `install-protoc.sh` in the above fashion. Simply invoking bash should resolve this issue, like so:
```
git clone https://github.com/SprocketBot/carball
cd carball/
bash ./_travis/install-protoc.sh
python init.py
```
Apple's decision to replace bash as the default shell may foreshadow the removal of bash in a future version of MacOS. In such a case, Homebrew users can [install protoc](http://google.github.io/proto-lens/installing-protoc.html) by replacing `bash ./travis/install-protoc.sh` with `brew install protobuf`.


## Examples / Usage
One of the main data structures used in carball is the pandas.DataFrame, to learn more, see [its wiki page](https://github.com/SaltieRL/carball/wiki/data_frame).

Decompile and analyze a replay:
```Python
import carball

analysis_manager = carball.analyze_replay_file('9EB5E5814D73F55B51A1BD9664D4CBF3.replay', 
                                      output_path='9EB5E5814D73F55B51A1BD9664D4CBF3.json', 
                                      overwrite=True)
proto_game = analysis_manager.get_protobuf_data()

# you can see more example of using the analysis manager below

```

Just decompile a replay to a JSON object:

```Python
import carball

_json = carball.decompile_replay('9EB5E5814D73F55B51A1BD9664D4CBF3.replay', 
                                output_path='9EB5E5814D73F55B51A1BD9664D4CBF3.json', 
                                overwrite=True)
```

Analyze a JSON game object:
```Python
import carball
import gzip
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

# _json is a JSON game object (from decompile_replay)
game = Game()
game.initialize(loaded_json=_json)

analysis_manager = AnalysisManager(game)
analysis_manager.create_analysis()
    
# return the proto object in python
proto_object = analysis_manager.get_protobuf_data()

# return the proto object as a json object
json_oject = analysis_manager.get_json_data()

# return the pandas data frame in python
dataframe = analysis_manager.get_data_frame()
```

You may want to save carball analysis results for later use:

```python
# write proto out to a file
# read api/*.proto for info on the object properties
with open('output.pts', 'wb') as fo:
    analysis_manager.write_proto_out_to_file(fo)
    
# write pandas dataframe out as a gzipped numpy array
with gzip.open('output.gzip', 'wb') as fo:
    analysis_manager.write_pandas_out_to_file(fo)
```

Read the saved analysis files:

```python
import gzip
from carball.analysis.utils.pandas_manager import PandasManager
from carball.analysis.utils.proto_manager import ProtobufManager

# read proto from file
with open('output.pts', 'rb') as f:
    proto_object = ProtobufManager.read_proto_out_from_file(f)

# read pandas dataframe from gzipped numpy array file
with gzip.open('output.gzip', 'rb') as f:
    dataframe = PandasManager.read_numpy_from_memory(f)
```

### Command Line

Carball comes with a command line tool to analyze replays. To use carball from the command line:

```bash
carball -i 9EB5E5814D73F55B51A1BD9664D4CBF3.replay --json analysis.json
```

To get the analysis in both json and protobuf and also the compressed replay frame data frame:

```bash
carball -i 9EB5E5814D73F55B51A1BD9664D4CBF3.replay --json analysis.json --proto analysis.pts --gzip frames.gzip
```

#### Command Line Arguments

```
usage: carball [-h] -i INPUT [--proto PROTO] [--json JSON] [--gzip GZIP] [-sd]
               [-v] [-s]

Rocket League replay parsing and analysis.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to replay file that will be analyzed. Carball
                        expects a raw replay file unless --skip-decompile is
                        provided.
  --proto PROTO         The result of the analysis will be saved to this file
                        in protocol buffers format.
  --json JSON           The result of the analysis will be saved to this file
                        in json file format.
  --gzip GZIP           The pandas dataframe will be saved to this file in a
                        compressed gzip format.
  -v, --verbose         Set the logging level to INFO. To set the logging
                        level to DEBUG use -vv.
  -s, --silent          Disable logging altogether.
```

## Pipeline
![pipeline is in Parserformat.png](Parser%20format.png)

If you want to add a new stat it is best to do it in the advanced stats section of the pipeline.
You should look at:

[Stat base classes](carball/analysis/stats/stats.py)

[Where you add a new stat](carball/analysis/stats/stats_list.py)

If you want to see the output format of the stats created you can look [here](api)

Compile the proto files by running in this directory
`setup.bat` (Windows) or `setup.sh` (Linux/mac)

[![Build Status](https://travis-ci.org/SaltieRL/carball.svg?branch=master)](https://travis-ci.org/SaltieRL/carball)
[![codecov](https://codecov.io/gh/SaltieRL/carball/branch/master/graph/badge.svg)](https://codecov.io/gh/SaltieRL/carball)
