تحميل Hadoop
wget https://archive.apache.org/dist/hadoop/core/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xvzf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
nano ~/.bashrc
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
source ~/.bashrc



export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

nano pom.xml
nano src/main/java/spark/batch/tp21/WordCountTask.java



cd ~/wordcount-spark
mkdir -p input
cp ~/purchases.txt input/


ls input


spark-submit:
spark-submit \
  --class spark.batch.tp21.WordCountTask \
  --master local \
  target/wordcount-spark-1.0-SNAPSHOT.jar \
  input/purchases.txt \
  out-spark-java


ls out-spark-java
cat out-spark-java/part-00000


 nano input/purchases.txt
 cp purchases.txt input/
 cat input/purchases.txt

cd ~/wordcount-spark

spark-submit \
  --class spark.batch.tp21.WordCountTask \
  --master local \
  target/wordcount-spark-1.0-SNAPSHOT.jar \
  input/purchases.txt \
  out-spark-java

Spark Streaming :

mkdir ~/stream-spark
cd ~/stream-spark

pwd

mkdir -p src/main/java/spark/streaming/tp22

3) إنشاء ملف pom.xml

nano pom.xml

<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>spark.streaming</groupId>
    <artifactId>stream</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-core_2.13</artifactId>
            <version>3.5.0</version>
        </dependency>

        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-sql_2.13</artifactId>
            <version>3.5.0</version>
        </dependency>

        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-streaming_2.13</artifactId>
            <version>3.5.0</version>
        </dependency>
    </dependencies>
</project>


4) إنشاء ملف Java: Stream.java

nano src/main/java/spark/streaming/tp22/Stream.java

package spark.streaming.tp22;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Encoders;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import org.apache.spark.sql.streaming.Trigger;

import java.util.Arrays;
import java.util.concurrent.TimeoutException;

public class Stream {

    public static void main(String[] args) throws StreamingQueryException, TimeoutException {

        SparkSession spark = SparkSession
                .builder()
                .appName("NetworkWordCount")
                .master("local[*]")
                .getOrCreate();

        Dataset<String> lines = spark
                .readStream()
                .format("socket")
                .option("host", "localhost")
                .option("port", 9999)
                .load()
                .as(Encoders.STRING());

        Dataset<String> words = lines.flatMap(
                (String x) -> Arrays.asList(x.split("\\s+")).iterator(),
                Encoders.STRING()
        );

        Dataset<Row> wordCounts = words.groupBy("value").count();

        StreamingQuery query = wordCounts.writeStream()
                .outputMode("complete")
                .format("console")
                .trigger(Trigger.ProcessingTime("1 second"))
                .start();

        query.awaitTermination();
    }
}

5) بناء المشروع (compile)
cd ~/stream-spark
mvn package

6) تشغيل Spark Streaming
nc -lk 9999

نافذة 2 — شغّل Streaming:
  
cd ~/stream-spark

spark-submit \
  --class spark.streaming.tp22.Stream \
  --master local \
  target/stream-1.0-SNAPSHOT.jar

