import urllib.request
import re

try:
    html = urllib.request.urlopen('https://sistem-pakar2.vercel.app').read().decode('utf-8')
    script_url_match = re.search(r'src="(/assets/index-[^"]+\.js)"', html)
    if not script_url_match:
        print("Could not find JS bundle")
        exit(1)
        
    script_url = script_url_match.group(1)
    js = urllib.request.urlopen('https://sistem-pakar2.vercel.app' + script_url).read().decode('utf-8')
    
    matches = re.findall(r'https://[^"]+railway\.app/?', js)
    print("RAILWAY URL IN JS:", list(set(matches)))
except Exception as e:
    print("Error:", e)
