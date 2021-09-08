import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0,module)

from netkiller.docker import *

if __name__ == '__main__':

	volume = Volumes('redis')

	# network = Networks('production')
	# network.driver()
	network = Networks()
	network.driver().ipam().driver().config(['subnet: 172.33.10.0/24','gateway: 172.33.10.1'])

	service =  Services('nginx')
	service.image('nginx:latest')
	service.container_name('nginx')
	service.restart('always')
	service.hostname('www.netkiller.cn')
	service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
	service.environment(['TA=Asia/Shanghai'])
	service.ports(['8080:8080'])
	service.volumes(['/tmp/test:/tmp'])
	service.command(['--server.port=8080','--spring.profiles.active=default'])
	# service.debug()
	# print()
	# service.dump()

	sms =  Services('sms')
	sms.image('nginx:latest')
	sms.container_name('nginx')
	sms.restart('always')
	sms.hostname('www.netkiller.cn')

	

	compose = Composes('development')
	compose.version('3.9')
	compose.services(service)
	compose.services(sms)
	compose.networks(network)
	# compose.networks(mynet)
	compose.volumes(volume)
	compose.workdir('/tmp/compose')
	# print(environment.debug())
	# compose.environment('development').version("3.8").services(sms)
	# compose.execute()
	# print (compose.debug())
	print(compose.dump())
	# compose.up()
	# compose.up(True,'sms')
	# compose.start('api')
	# compose.restart('api')
	# compose.logs('api')

	test = Composes('testing')
	test.version('3.9')
	test.services(sms)

	# docker = Docker()
	# docker.environment(compose)
	# docker.environment(test)
	# docker.dump()
	# docker.up()


	try:
		docker = Docker()
		docker.environment(compose)
		docker.main()
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")