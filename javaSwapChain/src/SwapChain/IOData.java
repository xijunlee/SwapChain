package SwapChain;

import java.io.*;

public class IOData {
	public static void read_data(Providers P[],Customer O[],String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //����һ��FileReader����   �Ӵ��̶�
		       BufferedReader br = new BufferedReader(fr);    //����һ��BufferedReader����

		       String line = "";                   //����һ��String����line������ÿ�ζ�һ�еĽ��
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //����ļ�׼���ã��ͼ�����
		         line=br.readLine();//��һ��
		         a[lineCount] = new String[line.split("\t").length];
		         a[lineCount] = line.split("\t");
		         lineCount++;
		       }
		       br.close();                                   //�ر���
		       fr.close();                                   //�ر���
		       
		       //��ʼ��providers,customers
		       Providers[] p = new Providers[Integer.parseInt(a[0][0])];
		       //����ֻ�ǳ�ʼ�������ã���û��������ʼ���Ķ���
		       Customer[] o = new Customer[Integer.parseInt(a[p.length+1][0])];
		       //���������������������provider������
		       for (int i=1;i<=p.length;i++)
		       {
		    	  p[i-1]=new Providers();//����ÿ�����ã���Ҫ��ʼ��ʵ�����󣬽��丳������
		    	  p[i-1].x=Double.parseDouble(a[i][0]);
		    	  p[i-1].y=Double.parseDouble(a[i][1]);
		    	  p[i-1].CapacityCtr=Integer.parseInt(a[i][2]);
		    	  p[i-1].capacity = new double[p[i-1].CapacityCtr];
		    	  for (int j=0;j<p[i-1].CapacityCtr;j++)
		    		  p[i-1].capacity[j]=Double.parseDouble(a[i][j+3]);
		       }
		       //���������������������customer������
		       for (int i=p.length+2,k=0;i<lineCount;i++)
		       {
		          o[k]=new Customer();
		    	  o[k].x=Double.parseDouble(a[i][0]);
		          o[k].y=Double.parseDouble(a[i][1]);
		          o[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		       
		       /*for (int i=0;i<o.length;i++)
		       {
		    	   System.out.print(o[i].x+" ");
		    	   System.out.print(o[i].y+" ");
		    	   System.out.println(o[i].Demand+" ");
		       }*/
		       
		       P=p;O=o;
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
		
	}
	
}
