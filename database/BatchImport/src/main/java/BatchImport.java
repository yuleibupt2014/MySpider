import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;


public class BatchImport {
    private static Configuration conf = null;

    /**
     * 初始化配置
     */
    static {
        conf = HBaseConfiguration.create();
        conf.addResource(new Path("/software/servers/hbase-0.98.11-hadoop2/conf/core-site.xml"));
        conf.addResource(new Path("/software/servers/hbase-0.98.11-hadoop2/conf/hbase-site.xml"));
        conf.addResource(new Path("/software/servers/hbase-0.98.11-hadoop2/conf/hdfs-site.xml"));
    }

//    public static boolean isNumeric(String str){
//        for(int i=str.length();--i>=0;){
//            int chr=str.charAt(i);
//            if(chr<48 || chr>57)
//                return false;
//        }
//        return true;
//    }

    static class HbaseMapper extends Mapper<LongWritable, Text, Text, Text> {
        private Text rowkey = new Text();
        private Text category = new Text();

        public void map(LongWritable offset, Text line, Context context)
                throws IOException, InterruptedException {
            String[] labels = line.toString().trim().split(",");
            if(labels.length == 4){
                rowkey.set(labels[3]);
                category.set(labels[0] + "," + labels[1] + "," + labels[2] + "," + labels[3]);
                context.write(rowkey, category);
            }
        }
    }

    public static class HbaseReducer extends
            TableReducer<Text, Text, ImmutableBytesWritable> {

        public void reduce(Text key, Iterable<Text> values,
                           Context context) throws IOException, InterruptedException {
            for (Text val : values) {
                Put put = new Put(Bytes.toBytes(key.toString()));
                String[] labels = val.toString().split(",");
                if (labels.length == 4){
                    if (labels[0].isEmpty()){
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labelone"), Bytes.toBytes(labels[1]));
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labeltwo"), Bytes.toBytes(labels[2]));
                    }else if (labels[1].isEmpty()){
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labelone"), Bytes.toBytes(labels[0]));
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labeltwo"), Bytes.toBytes(labels[2]));
                    } else  if(labels[2].isEmpty()){
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labelone"), Bytes.toBytes(labels[0]));
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labeltwo"), Bytes.toBytes(labels[1]));
                    } else{
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labelone"), Bytes.toBytes(labels[0]));
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labeltwo"), Bytes.toBytes(labels[1]));
                        put.add(Bytes.toBytes("category"), Bytes.toBytes("labelthree"), Bytes.toBytes(labels[2]));
                    }
                }
                context.write(new ImmutableBytesWritable(key.getBytes()), put);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        conf.set("mapreduce.job.queuename", "ven2");
        conf.set("fs.defaultFS", "hdfs://ecloudtest");
        String tablename = "jd_user";
        HBaseAdmin admin = new HBaseAdmin(conf);
        if(admin.tableExists(tablename)){
            System.out.println("table exists!recreating.......");
            admin.disableTable(tablename);
            admin.deleteTable(tablename);
        }
        HTableDescriptor htd = new HTableDescriptor(TableName.valueOf(tablename));
        HColumnDescriptor tcd = new HColumnDescriptor("category");
        htd.addFamily(tcd);
        admin.createTable(htd);

        Job job = Job.getInstance(conf, "WriteToHbase");
        job.setJarByClass(BatchImport.class);
        job.setMapperClass(HbaseMapper.class);
        job.setReducerClass(HbaseReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputFormatClass(TableOutputFormat.class);
        job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, "jd_user");
        job.setOutputKeyClass(ImmutableBytesWritable.class);
        TableMapReduceUtil.initTableReducerJob(tablename, HbaseReducer.class, job);
        // job.setNumReduceTasks(0);
        FileInputFormat.addInputPath(job, new Path("hdfs://ecloudtest/user/vendorbupt/wtist/jd/*"));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
