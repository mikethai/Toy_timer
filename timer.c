#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <strings.h>

struct TMR {
	char tag[16];
	int ticks;
	void (*func)();
	struct TMR *pnext;
};

typedef struct TMR Timer;
Timer *phead;
time_t myclock;

time_t initTimer(){
	struct tm time_str;
	time_str.tm_year    = 2015 - 1900;
	time_str.tm_mon = 5 - 1;
	time_str.tm_mday = 6;
	time_str.tm_hour = 0;
	time_str.tm_min = 0;
	time_str.tm_sec = 0;
	time_str.tm_isdst = -1;
	return mktime(&time_str);
}
Timer *createTimer(char*ptag, int ticks, void(*func)()){
	Timer *ptmr;
	ptmr=(Timer*)malloc(sizeof(struct TMR));
	strcpy(ptmr->tag, ptag);
	ptmr->ticks=ticks;
	ptmr->pnext=0;
	ptmr->func=func;
	return ptmr;
}
void dumpTimer(){
	Timer *ptmr=phead;
	int t=0;
	printf("Dump timer chain at %s", ctime(&myclock));
	while(ptmr) {
		t+=ptmr->ticks;
		printf("Timer %s: has %d/%d ticks left.\n", ptmr->tag, ptmr->ticks, t);
		ptmr=ptmr->pnext;
	}
	if(phead==0) printf("Timer chain is empty!\n");	
}
void insertTimer(Timer*ptmr){
	Timer*pprev=0;
	Timer*p=phead;
	int t=ptmr->ticks;
	while(p && p->ticks<t) {
		t-=p->ticks;
		pprev=p;
		p=p->pnext;
	}
	if(p) p->ticks-=t;
	ptmr->ticks=t;
	ptmr->pnext=p;
	if(pprev) pprev->pnext=ptmr;
	else phead=ptmr;
}
int removeTimer(char*pname){
	Timer*pprev=0;
	Timer*ptmr=phead;
	while(ptmr) {
		if(strcmp(ptmr->tag,pname)==0) break;
		pprev=ptmr;
		ptmr=ptmr->pnext;
	}
	if(ptmr){
		if(pprev) pprev->pnext=ptmr->pnext;
		else phead=ptmr->pnext;
		if(ptmr->pnext)
			ptmr->pnext->ticks+=ptmr->ticks;
		free(ptmr);
		return 1;
	}
	return 0;
}
void myworld(char *event){
	printf("Run event %s: We are the world! at %s", 
		event, ctime(&myclock));
}
void mytrust(char *event){
	printf("Run event %s: Trust me! You can make it! at %s", 
		event, ctime(&myclock));
}
void mydoit(char *event){
	printf("Run event %s: Just do it now! at %s", 
		event, ctime(&myclock));
}
void (*dofunc[])()={myworld, mytrust, mydoit};
void runto(int ticks){
	static int tickcount=0;
	Timer*ptmr;
	while(tickcount<ticks) {
		if(phead){
			phead->ticks--;
			myclock++;
			while(phead && phead->ticks==0) {
				printf("Timer %s is timeout at %s", phead->tag, ctime(&myclock));
				ptmr = phead;
				(*phead->func)(phead->tag);
				phead = phead->pnext;
				free(ptmr);
			}
		}
		tickcount++;
	}
}
void run(){
	int ticks,seconds,fid;
	char cmd[16], event[16];
	myclock = initTimer();
	printf("System starts at %s", ctime(&myclock));
	for(;;){
		scanf("%d%s", &ticks, cmd);
		runto(ticks);
		if(cmd[0]=='e') break;
		switch(cmd[0]){
		case 'i':
			scanf("%s%d%d", event, &seconds, &fid);
			insertTimer(createTimer(event,seconds,dofunc[fid]));
			break;
		case 'r':
			scanf("%s", event);
			removeTimer(event);
			break;
		case 'd':
			dumpTimer();
		}
	}
	printf("System stops at %s", ctime(&myclock));
}
main(){
	run();
}
