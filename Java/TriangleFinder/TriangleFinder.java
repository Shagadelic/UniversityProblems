package bigdata;

import com.google.common.collect.Iterables;
import org.apache.spark.InternalAccumulator;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class TriangleFinder {
    public static void main(String [] args){
        SparkConf conf = new SparkConf().setAppName("TriangleFinder");
        JavaSparkContext sc = new JavaSparkContext(conf);

        //lines of edges, cached because its used in step 1 and 2
        JavaRDD<String[]> inputRDD = sc.textFile(args[0]).map(l->l.split("\t")).cache();
        //RDD with existing edges
        JavaPairRDD<Tuple2<String, String>, String> existingEdge = inputRDD.mapToPair(l -> new Tuple2<Tuple2<String, String>, String>(new Tuple2<String, String> (l[0], l[1]) , "$"));

        //map1 output part1: vertex left with its neighbour on the right1
        JavaPairRDD <String, String> map1leftright = inputRDD.mapToPair(edgePair->new Tuple2<String, String>(edgePair[0], edgePair[1]));

        //map1 output part2: vertex on the right with its neighbour to the left
        JavaPairRDD <String, String> map1rightleft = inputRDD.mapToPair(edgePair->new Tuple2<String, String>(edgePair[1], edgePair[0]));

        //map1 combined output.
        //each vertex with its neighbourhood: (v2, [v1, v3, v4, v5])
        JavaPairRDD <String, Iterable<String>> map1 = map1leftright.union(map1rightleft).groupByKey();

        //reduce 1
        //removes vertices with just 1 neighbour
        JavaPairRDD <Tuple2<String, String>, String> red1 = map1.filter(l -> Iterables.size(l._2()) > 1)
                //two-paths from v1 to v2 over vertex u ((v1, v2), u)
                .flatMapToPair(l->{

                    List< Tuple2<Tuple2<String, String>, String> > res = new ArrayList< Tuple2<Tuple2<String, String>, String> >();


                    //converts iterable to list
                    List<String> neighbours = new ArrayList<String>();
                    for(String neighbour : l._2()){
                        neighbours.add(neighbour);
                    }
                    //creates pair combinations of u's neighbours
                    for(int i=0; i<neighbours.size(); i++){
                        for(int j=i+1; j<neighbours.size(); j++){

                            Tuple2<String,String> pair = new Tuple2<String,String>(neighbours.get(i), neighbours.get(j));
                            Tuple2<Tuple2<String,String>, String> element = new Tuple2<Tuple2<String,String>, String>(pair, l._1());

                            res.add(element);

                        }
                    }
                    return res.iterator();
                });
        // ((from, to), [reachable over v1, v2..., + "$" if edge from <-> to exists])
        JavaPairRDD<Tuple2<String, String>, Iterable<String>> map2 = red1.union(existingEdge).groupByKey();
        //removes lists without $, so only K,Vs with triangles are left
        JavaPairRDD<Tuple2<String, String>, Iterable<String>> map2WithEdge = map2.filter(
                l->{
                        for(String v : l._2()){

                            if(v.equals("$")){

                                return true;
                            }
                        }

                  return false;
                });

        //result
        JavaRDD<String> result = map2WithEdge.flatMap(s->{
            List<String> res = new ArrayList<String>();
            List<String> temp = new ArrayList<String>();
            for(String u: s._2()){
                if(!u.equals("$")){
                    //adds key nodes with existing edge and a connecting node
                    temp.add(s._1()._1());
                    temp.add(s._1()._2());
                    temp.add(u);
                    //sorts nodes (to filter distinct triangles later)
                    Collections.sort(temp);
                    StringBuilder builder = new StringBuilder();
                    builder.append(temp.get(0)+"\t"+temp.get(1)+"\t"+temp.get(2));
                    //adds triangle to result
                    res.add(builder.toString());
                }
                temp.clear();
            }
            return res.iterator();
            //removes duplicate triangles
        }).distinct();

        result.saveAsTextFile(args[1]);
    }
}
