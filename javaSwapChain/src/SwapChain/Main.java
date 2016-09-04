package SwapChain;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static Providers P[];
    public static Provider Ps[];
    public static Customer O[];
    public static final int max_size=10000;
	public static void main(String[] args) throws Exception {
        //Ҫ˫б�ܣ�����б��+��ĸ�ᱻ������ʶ���ת���ַ�
		//ReadData("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\alldata.txt");
	    /*GA ga = new GA(P,O,100);//������������׼���������D
	    ga.Solver();*/
//	    NSGAII nsga = new NSGAII(P,O);
//	    nsga.Solver();
		ReadDataForSwapChain("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\pydata.txt");
		SwapChainSolver sc = new SwapChainSolver(Ps,O);
		double mmd=sc.Solver();
        System.out.println(mmd);
	
       /* ReadData("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\alldata.txt");
		SearchOptimal so=new SearchOptimal(P,O,10);//������������׼��ƥ���������D
		so.GetTheOptimal();*/
	}
	
	public static void ReadDataForSwapChain(String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //����һ��FileReader����   �Ӵ��̶�
		       BufferedReader br = new BufferedReader(fr);    //����һ��BufferedReader����

		       String line = "";                   //����һ��String����line������ÿ�ζ�һ�еĽ��
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //����ļ�׼���ã��ͼ�����
		         line=br.readLine();//��һ��
		         a[lineCount] = new String[line.split(" ").length];
		         a[lineCount] = line.split(" ");
		         lineCount++;
		       }
		       br.close();                                   //�ر���
		       fr.close();                                   //�ر���
		       
		       //��ʼ��providers,customers
		       Ps = new Provider[Integer.parseInt(a[0][0])];
		       //����ֻ���������������ã���û��ʵ��������
		       O = new Customer[Integer.parseInt(a[Ps.length+1][0])];
		       //���������������������provider������
		       for (int i=1;i<=Ps.length;i++)
		       {
		    	  Ps[i-1]=new Provider();//ʵ�������󣬲������󴫸���Ӧ����
		    	  Ps[i-1].x=Double.parseDouble(a[i][0]);
		    	  Ps[i-1].y=Double.parseDouble(a[i][1]);
                  Ps[i-1].Capacity=Double.parseDouble(a[i][2]);
		       }
		       //���������������������customer������
		       for (int i=Ps.length+2,k=0;i<lineCount;i++)
		       {
		          O[k]=new Customer();
		    	  O[k].x=Double.parseDouble(a[i][0]);
		          O[k].y=Double.parseDouble(a[i][1]);
		          O[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
	}
	
	public static void ReadData(String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //����һ��FileReader����   �Ӵ��̶�
		       BufferedReader br = new BufferedReader(fr);    //����һ��BufferedReader����

		       String line = "";                   //����һ��String����line������ÿ�ζ�һ�еĽ��
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //����ļ�׼���ã��ͼ�����
		         line=br.readLine();//��һ��
		         a[lineCount] = new String[line.split(" ").length];
		         a[lineCount] = line.split(" ");
		         lineCount++;
		       }
		       br.close();                                   //�ر���
		       fr.close();                                   //�ر���
		       
		       //��ʼ��providers,customers
		       P = new Providers[Integer.parseInt(a[0][0])];
		       //����ֻ���������������ã���û��ʵ��������
		       O = new Customer[Integer.parseInt(a[P.length+1][0])];
		       //���������������������provider������
		       for (int i=1;i<=P.length;i++)
		       {
		    	  P[i-1]=new Providers();//ʵ�������󣬲������󴫸���Ӧ����
		    	  P[i-1].x=Double.parseDouble(a[i][0]);
		    	  P[i-1].y=Double.parseDouble(a[i][1]);
		    	  P[i-1].CapacityCtr=Integer.parseInt(a[i][2]);
		    	  P[i-1].capacity = new double[P[i-1].CapacityCtr];
		    	  P[i-1].cost = new double[P[i-1].CapacityCtr];
		    	  for (int j=0;j<P[i-1].CapacityCtr;j++)
		    	  {
		    		  P[i-1].capacity[j]=Double.parseDouble(a[i][j+3]);
		    		  P[i-1].cost[j]=Double.parseDouble(a[i][j+3+P[i-1].CapacityCtr]);
		    	  }
		    	  
		       }
		       //���������������������customer������
		       for (int i=P.length+2,k=0;i<lineCount;i++)
		       {
		          O[k]=new Customer();
		    	  O[k].x=Double.parseDouble(a[i][0]);
		          O[k].y=Double.parseDouble(a[i][1]);
		          O[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
	}
}
