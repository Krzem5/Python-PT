import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.lang.Class;
import java.lang.ClassLoader;
import java.util.ArrayList;



public class Main{
	public static final String SCRIPT_DIRECTORY="./scripts/";
	public Script[] SCRIPTS;



	public Main(){
		this.SCRIPTS=this._load();
		for (Script s:this.SCRIPTS){
			s.exec();
		}
	}



	private Script[] _load(){
		try{Object o=new ModuleLoader().loadClass(".\\scripts\\scriptA.java");return new Script[]{o};}catch( Exception e){e.printStackTrace();}return null;
	}



	public static void main(String[] args){
		new Main();
	}
}



class ModuleLoader extends ClassLoader{
	@Override
	public Class<?> findClass(String nm) throws ClassNotFoundException{
		try{
			return this._load(nm);
		}
		catch (Exception e){
			e.printStackTrace();
		}
		return null;
	}



	private Class<?> _load(String nm) throws IOException,InterruptedException{
		String dir=nm.substring(0,nm.lastIndexOf("\\"));
		String sp=System.getProperty("user.dir");
		String fn=nm.substring(nm.lastIndexOf("\\")+1);
		ProcessBuilder b=new ProcessBuilder("cmd.exe","/c","cd \""+dir+"\"&&javac -sourcepath "+sp+" "+fn);
		b.inheritIO();
		Process p=b.start();
		p.waitFor();
		InputStream inpS=new FileInputStream(new File(dir+"\\"+fn.replace(".java",".class")));
		ByteArrayOutputStream bS=new ByteArrayOutputStream();
		int cb=-1;
		while ((cb=inpS.read())!=-1){
			bS.write(cb);
		}
		byte[] bl=bS.toByteArray();
		String name=fn.replace(".java","");
		return this.defineClass(name,bl,0,bl.length);
	}
}