# Demo

### Dependency

The loglizer toolkit is implemented with Python and requires a number of dependency requirements installed. 

+ python 3.6
+ scipy
+ numpy
+ scikit-learn=0.20.3
+ pandas

We recommend users to use Anaconda, which is a popular Python data science platform with many common packages pre-installed. The virtual enviorment can be set up via `conda`:

```
$ conda create -n py36 -c anaconda python=3.6
$ conda activate py36
```

For ease of reproducing our benchmarking results, we have also built a docker image for the running evironment. If you have docker installed, you can easily pull and run a docker container as follows:

```
$ mkdir loglizer
$ git clone https://github.com/logpai/loglizer.git loglizer/
$ docker run --name loglizer -v loglizer:/loglizer -it logpai/anaconda:py3.6 bash
$ cd /loglizer/demo
```

### Run loglizer

You can try the demo scripts of loglizer on different structured log datasets by specifying the `--dataset` command line argument.

#### New: `--dataset` parameter

We have added a `--dataset` argument to allow switching between multiple datasets. Please use it to specify which structured log file to analyze. For example:

```bash
$ python PCA_demo.py --dataset HDFS
$ python InvariantsMiner_demo.py --dataset HDFS100k
```

#### Available dataset options

| Dataset name | Description               | Structured log path                                               |
| ------------ | ------------------------- | ----------------------------------------------------------------- |
| HDFS100k     | Special full HDFS dataset | `../data/HDFS/HDFS_100k.log_structured.csv`                       |
| HDFS         | 2k version of HDFS logs   | `../data/loghub_2k/HDFS/HDFS_2k.log_structured.csv`               |
| Apache       | 2k Apache logs            | `../data/loghub_2k/Apache/Apache_2k.log_structured.csv`           |
| Android      | 2k Android logs           | `../data/loghub_2k/Android/Android_2k.log_structured.csv`         |
| BGL          | 2k BGL logs               | `../data/loghub_2k/BGL/BGL_2k.log_structured.csv`                 |
| HPC          | 2k HPC logs               | `../data/loghub_2k/HPC/HPC_2k.log_structured.csv`                 |
| Hadoop       | 2k Hadoop logs            | `../data/loghub_2k/Hadoop/Hadoop_2k.log_structured.csv`           |
| HealthApp    | 2k HealthApp logs         | `../data/loghub_2k/HealthApp/HealthApp_2k.log_structured.csv`     |
| Linux        | 2k Linux logs             | `../data/loghub_2k/Linux/Linux_2k.log_structured.csv`             |
| Mac          | 2k Mac logs               | `../data/loghub_2k/Mac/Mac_2k.log_structured.csv`                 |
| OpenSSH      | 2k OpenSSH logs           | `../data/loghub_2k/OpenSSH/OpenSSH_2k.log_structured.csv`         |
| OpenStack    | 2k OpenStack logs         | `../data/loghub_2k/OpenStack/OpenStack_2k.log_structured.csv`     |
| Proxifier    | 2k Proxifier logs         | `../data/loghub_2k/Proxifier/Proxifier_2k.log_structured.csv`     |
| Spark        | 2k Spark logs             | `../data/loghub_2k/Spark/Spark_2k.log_structured.csv`             |
| Thunderbird  | 2k Thunderbird logs       | `../data/loghub_2k/Thunderbird/Thunderbird_2k.log_structured.csv` |
| Windows      | 2k Windows logs           | `../data/loghub_2k/Windows/Windows_2k.log_structured.csv`         |
| Zookeeper    | 2k Zookeeper logs         | `../data/loghub_2k/Zookeeper/Zookeeper_2k.log_structured.csv`     |

> **Note:** If `--dataset` is not provided, the default will be `HDFS100k`.