
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.Arrays;

public class WordCountTask {

    public static void main(String[] args) {

        if (args.length < 2) {
            System.err.println("Usage: WordCountTask <inputPath> <outputPath>");
            System.exit(1);
        }

        String inputPath = args[0];
        String outputPath = args[1];

        new WordCountTask().run(inputPath, outputPath);
    }

    public void run(String inputFilePath, String outputDir) {

        // إعداد Spark لتشغيل في الوضع المحلي
        SparkConf conf = new SparkConf()
                .setAppName(WordCountTask.class.getName())
                .setMaster("local[*]");

        // إنشاء الـ SparkContext
        JavaSparkContext sc = new JavaSparkContext(conf);

        // قراءة الملف من HDFS أو من النظام حسب المسار
        JavaRDD<String> textFile = sc.textFile(inputFilePath);

        // تحويل النص إلى كلمات وإحصاء التكرارات
        JavaPairRDD<String, Integer> counts = textFile
                .flatMap(s -> Arrays.asList(s.split("\\s+")).iterator())
                .mapToPair(word -> new Tuple2<>(word, 1))
                .reduceByKey(Integer::sum);

        // حفظ النتيجة في HDFS
        counts.saveAsTextFile(outputDir);

        // إغلاق السياق
        sc.close();
    }
}
