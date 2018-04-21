
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
import org.apache.hadoop.io.MapWritable;
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

public class TwitterPolarity {
	
	private static final Map<String, Double> dictionary = new HashMap<String, Double>();
	

	/*
	 *  dictionary stored in hashmap: key is tweet, value is polarity
	 */
	public static void readToHashMap() throws NumberFormatException, IOException{
		BufferedReader in =  new BufferedReader(new FileReader("../data/all/dictionary.v4.txt"));
		String line = "";
		line = in.readLine();
		while((line = in.readLine()) != null){
			String parts[] = line.split("\t");
			dictionary.put(parts[0], Double.parseDouble(parts[1]));
		}
		in.close();
	}

	/*
	 *  Mapper: <Text(tweet), MapWritable<dict_word, polarity>>
	 */
  public static class PolarityMapper extends MapReduceBase
      implements Mapper<LongWritable, Text, Text, MapWritable> {

	private final static String REGEX = "([a-zA-Z]+)"; //only match words with 1 or more characters
	private final static MapWritable map = new MapWritable();
    
    public void map(LongWritable key, Text val,
        OutputCollector<Text, MapWritable> output, Reporter reporter)
        throws IOException {

     
      Pattern p = Pattern.compile(REGEX);
      String line = val.toString();
      String words[] = line.split(" ");
      
      //Check for dictionary words in tweet and store in map
      for(int i = 0; i < words.length; i++){
    	  Matcher m = p.matcher(words[i]);
    	  if(m.find()){
    		  if(dictionary.containsKey(m.group(0))){
    			  Text k = new Text(m.group(0));
    			  if(!map.containsKey(k))
    				  map.put(k, new DoubleWritable(dictionary.get(m.group(0))));
    			  
    		  }
    	  }
      }
      
      
      output.collect(new Text(line), map);
    }
  }


  /*
   * Reducer: <Text(tweet), DoubleWritable(average_polarity)>
   */
  public static class PolarityReducer extends MapReduceBase
      implements Reducer<Text, MapWritable, Text, DoubleWritable> {

    public void reduce(Text key, Iterator<MapWritable> values,
        OutputCollector<Text, DoubleWritable> output, Reporter reporter)
        throws IOException {

    	//get average polarity for each tweet
    	double avg = 0.0;
    	double sum = 0.0;
    	if(values.hasNext()){
    		MapWritable m = values.next();
    		Set<Writable> words = m.keySet();
    		for(Writable word : words){
    			DoubleWritable score = (DoubleWritable) m.get(word);
    			sum += score.get();
    		}
    		avg = sum/words.size();
    	}
    	
    	output.collect(key,  new DoubleWritable(avg));
    }
  }


  /**
   * The actual main() method for our program; this is the
   * "driver" for the MapReduce job.
   */
  public static void main(String[] args) throws Exception {
	  readToHashMap(); //read from dictionary file and store to hashmap
	  System.out.println(dictionary.toString());
	  System.out.println(dictionary.size());
	  
	//start of MapReduce job  
    JobConf conf = new JobConf(TwitterPolarity.class);
    conf.setJobName("MapReduce");
    
    conf.setMapOutputKeyClass(Text.class);
    conf.setMapOutputValueClass(MapWritable.class);
    conf.setOutputKeyClass(Text.class);
    conf.setOutputValueClass(DoubleWritable.class);
    
    conf.setMapperClass(PolarityMapper.class);
    conf.setReducerClass(PolarityReducer.class);
    
    conf.setInputFormat(TextInputFormat.class);
    conf.setOutputFormat(TextOutputFormat.class);
    
    FileInputFormat.setInputPaths(conf, new Path(args[0]));
    FileOutputFormat.setOutputPath(conf,  new Path(args[1]));
    
    JobClient.runJob(conf);
    
  }
}