package timer;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class timer {
	static int execute_time=0;
	static int phead_time=0;
	static List<Object> Time_ary = new ArrayList<Object>();
	
	static SimpleDateFormat dateFormatter = new  SimpleDateFormat("yyyy/MM/dd HH:mm:ss"); 
    static Calendar cal = Calendar.getInstance();
	
	public static void main(String[] args) throws IOException, ParseException { 
		
		Date firstTime = dateFormatter.parse("2015/01/01 00:00:00");
		cal.setTime(firstTime);
		
	    try {
	    	FileInputStream fis = new FileInputStream("timer.in");
	    	BufferedReader buf = new BufferedReader(new InputStreamReader(fis));	        

	    	for (String line = buf.readLine(); line != null; line = buf.readLine()){

	            try {
	            	String[] names=line.split(" ");	            

	            	int ticka =0;
	            	ticka = Integer.parseInt(names[0]);
	           	
	            	switch(names[1])
	            	{
	            	case "insert":
	            		String ptag0 = names[2];
	            		int ticks0 = Integer.parseInt(names[3]);
	            		int events0 = Integer.parseInt(names[4]);
	            		Timer_object object_name = new Timer_object(ptag0, ticks0, events0);
	            		Insert_Timer(object_name);
	            		break;
	            	case "dump":

	            		dumpTimer();
	            		break;
	            	case "remove":
	            		
	            		String ptag = names[2];
	            		removeTimer(ptag);
	            		break;
	            	}
	            runto(ticka);	

				} catch (Exception e) {
				}
	        }
	        buf.close();
	    } finally {
	    } 	    	
}

	public static void Insert_Timer(Timer_object object_name) {
		
		
		if (Time_ary.size()==0) {
			phead_time=Integer.parseInt(object_name.return_value("tick"));
			Time_ary.add(object_name);
		}else{
			if(phead_time > Integer.parseInt(object_name.return_value("tick"))){
				phead_time = Integer.parseInt(object_name.return_value("tick"));
				int head_time=Integer.parseInt(((Timer_object) Time_ary.get(0)).return_value("tick"));
				int new_time=Integer.parseInt(object_name.return_value("tick"));
				
				((Timer_object) Time_ary.get(0)).set_ticks(head_time-new_time);	
				//把陣列每個元素都往後一個
				Time_ary.add(object_name);
				int ary_length= Time_ary.size();
				for(int i= ary_length-2 ; i >= 0 ;i--){
					Object o = Time_ary.get(i); //o是原来的首元素
					Time_ary.set(i+1, o);
				}				
				Time_ary.set(0,object_name);
				
				}else{
					int head_time=Integer.parseInt(((Timer_object) Time_ary.get(0)).return_value("tick"));
					int new_time=Integer.parseInt(object_name.return_value("tick"));
					object_name.set_ticks(new_time-head_time);
					Time_ary.add(object_name);
				}
		}		
	}
	
	public static void removeTimer(String tag_name){
		for(int i = 0; i < Time_ary.size(); i++){
			if (((Timer_object) Time_ary.get(i)).return_value("tag").equals(tag_name)){
				Time_ary.remove(i);
			}
		}
	}
	
	public static void runto(int ticks){
		while (execute_time < ticks) {
			if (Time_ary.size()!=0) {
				((Timer_object) Time_ary.get(0)).cut_1s_ticks();
				cal.add(Calendar.SECOND, 1);                      //時間加為一秒
				while (Time_ary.size()!=0 && Integer.parseInt(((Timer_object) Time_ary.get(0)).return_value("tick"))==0) {
					System.out.println("Timer "+((Timer_object) Time_ary.get(0)).return_value("tag")+" at " + cal.getTime());
					DO_What(((Timer_object) Time_ary.get(0)).return_value("tag"), Integer.parseInt(((Timer_object) Time_ary.get(0)).return_value("events")));
					Time_ary.remove(0);
				}
				
			}
		execute_time+=1;	
		}
		
	}
	
	public static void dumpTimer(){
		int t=0;
		System.out.println("Dump timer chain at " + cal.getTime());
		for (Object obj : Time_ary) {
			t=t+Integer.parseInt(((Timer_object) obj).return_value("tick"));
			System.out.println("Timer "+ ((Timer_object) obj).return_value("tag") + ": has " + ((Timer_object) obj).return_value("tick") +"/"+ Integer.toString(t));
		}
	}
	
	public static void DO_What(String events,int num){
		switch (num) {
		case 0:
			System.out.println("Run events "+ events + " We are the world! at  " +cal.getTime());
			break;
		case 1:
			System.out.println("Run events "+ events + " Trust me! You can make it! at " +cal.getTime());
			break;
		case 2:
			System.out.println("Run events "+ events + " Just do it now! at " +cal.getTime());
			break;
		}
	}
}

class  Timer_object {
	String ptag;
	int ticks;
	int events;

	
	public Timer_object(String ptag2,int ticks2,int events2) {

		this.ptag = ptag2;
		this.ticks = ticks2;
		this.events = events2;
	}

	public void set_tag(String ptag){
		this.ptag = ptag;
	}
	
	public void set_ticks(int ticks){
		this.ticks = ticks;
	}
	
	public void cut_1s_ticks(){
		ticks = ticks-1;
	}
	
	public String return_value(String whi){
		switch (whi) {
		case "tag":
			whi = this.ptag;
			break;
		case "tick":
			whi = Integer.toString(this.ticks);
			break;
		case "events":
			whi = Integer.toString(this.events);
			break;
		}
		return whi;	
	}
	
	public void show_parmr(){
		System.out.println(this.ptag +" "+ Integer.toString(this.ticks) + " "+ Integer.toString(this.events));
	}
	
	
}




