#$mytime=Time.new(2015)
$mytime=Time.utc(2015,"jan",1,0,0,0)
$Timer_ary = Array.new(0)
$excute_time = 0
$phead_time = 0

def Do_What(events,num)
    case num
    when 0
    puts "Run events " + events + " :We are the world! at " + $mytime.to_s
    when 1
    puts "Run events " + events + " :Trust me! You can make it! at " + $mytime.to_s
    when 2
    puts "Run events " + events + ":Just do it now! at " + $mytime.to_s
    end
end 

def Insert_Timer(object_name)
    if $Timer_ary.length==0
       $phead_time= object_name.return_value("tick")    #第一個先push進來,當phead
       $Timer_ary.push(object_name)
    else
        if  $phead_time > object_name.return_value("tick") #如果比phead小
            $phead_time = object_name.return_value("tick")
            $Timer_ary[0].set_ticks($Timer_ary[0].return_value("tick")-object_name.return_value("tick"))
            $Timer_ary.unshift(object_name)
        else
            object_name.set_ticks(object_name.return_value("tick")-$Timer_ary[0].return_value("tick"))
            $Timer_ary.push(object_name)
        end
    end  
end

def removeTimer(tag_name)
    for obj in $Timer_ary
        if obj.return_value("tag") == tag_name
            $Timer_ary.delete(obj)
        end
    end
end

class Timer_Object
    def initialize(ptag ,ticks , events)
        @ptag=ptag
        @ticks=ticks
        @events=events
    end
    
    def set_tag(ptag)
        @ptag=ptag
    end
    def set_ticks(ticks)
        @ticks=ticks
    end
    def cut_1s_ticks()
        @ticks=@ticks-1
    end
    def set_events(events)
        @events=events
    end
    
    def return_value(whi)
        case whi
            when "tag"
                return @ptag
            when "tick"
                return @ticks
            when "events"
                return @events
        end        
    end
    
    def show_parmr
        puts @ptag,@ticks,@events
    end
end

def runto(ticks)
    while $excute_time < ticks 
    if $Timer_ary.length!=0
       $Timer_ary[0].cut_1s_ticks()
       $mytime = $mytime + (1)
       while $Timer_ary.length!=0 && $Timer_ary[0].return_value("tick") ==0
       puts "Timer  " + $Timer_ary[0].return_value("tag") + "  at " + $mytime.to_s
       Do_What($Timer_ary[0].return_value("tag"),$Timer_ary[0].return_value("events"))
       $Timer_ary.shift()
       end
    end
    $excute_time+=1
    end
end

def dumpTimer
    t=0
    puts "Dump timer chain at" + $mytime.to_s
    for obj in $Timer_ary
    t+=obj.return_value("tick")
    puts "Timer " + obj.return_value("tag").to_s + ": has " + obj.return_value("tick").to_s + "/" + t.to_s
    end
end

f = open("timer.in")
contents_array = []
f.each_line { |line| contents_array << line }
f.close

for param in contents_array
    param  = param.split(' ')
    ticka=param[0]
    
    case param[1]
        when "insert"
            object_name=param[2]
            object_ticks=param[3]
            object_evebt=param[4]
            object_name=Timer_Object.new(param[2],object_ticks.to_i,object_evebt.to_i)
            Insert_Timer(object_name)

        when "dump"
            dumpTimer()
        when "remove"
            removeTimer(param[2])
    end
    runto(ticka.to_i)
end