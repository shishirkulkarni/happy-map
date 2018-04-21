
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class AveragePolarity {
	
	private static final Map<String, Double> dictionary = new HashMap<String, Double>();
	

	
	/*
	 *  Mapper: <"all", polarity>
	 */
  public static class AverageMapper extends MapReduceBase
      implements Mapper<LongWritable, Text, Text, DoubleWritable> {

	private final static String REGEX = "(.*)\t(0.[0-9]+)"; //capture group 1 as polarity
	private final static Text all = new Text("all");
    
    public void map(LongWritable key, Text val,
        OutputCollector<Text, DoubleWritable> output, Reporter reporter)
        throws IOException {

     
      Pattern p = Pattern.compile(REGEX);
      Matcher m = p.matcher(val.toString());
    
      double polarity = 0.0;
      if(m.find()){
    	  polarity = Double.parseDouble(m.group(2));
      }
      
      
      output.collect(all, new DoubleWritable(polarity));
    }
  }

  

  /*
   * Reducer: <"all", avg polarity>
   */
  public static class AverageReducer extends MapReduceBase
      implements Reducer<Text, DoubleWritable, Text, DoubleWritable> {

    public void reduce(Text key, Iterator<DoubleWritable> values,
        OutputCollector<Text, DoubleWritable> output, Reporter reporter)
        throws IOException {

    	//polarity average
    	double sum = 0.0;
    	int count = 0;
    	while(values.hasNext()){
    		sum += values.next().get();
    		count++;
    	}
    	
    	output.collect(key,  new DoubleWritable(sum/count));
    }
  }


  /**
   * The actual main() method for our program; this is the
   * "driver" for the MapReduce job.
   */
  public static void main(String[] args) throws Exception {
	 
	//start of MapReduce job  
    JobConf conf = new JobConf(TwitterPolarity.class);
    conf.setJobName("Average");
    
    conf.setMapOutputKeyClass(Text.class);
    conf.setMapOutputValueClass(DoubleWritable.class);
    conf.setOutputKeyClass(Text.class);
    conf.setOutputValueClass(DoubleWritable.class);
    
    conf.setMapperClass(AverageMapper.class);
    conf.setReducerClass(AverageReducer.class);
    
    conf.setInputFormat(TextInputFormat.class);
    conf.setOutputFormat(TextOutputFormat.class);
    
    FileInputFormat.setInputPaths(conf, new Path(args[0]));
    FileOutputFormat.setOutputPath(conf,  new Path(args[1]));
    
    JobClient.runJob(conf);
    
  }
}