#-*- coding: utf-8 -*-
import os, sys
class Git():
	cmd = []
	def __init__(self, workspace = None, logger = None):
		self.logger = logger
		self.workspace = os.path.expanduser(workspace)
		if os.path.exists(self.workspace) :
			os.chdir(self.workspace)
			self.logger.info('workspace %s' % self.workspace)
		else:
			self.logger.info("directory doesn't exist %s" % self.workspace)
			exit(0)
		self.logger.info('project directory %s' % os.getcwd())
		
	def option(self, opt):
		if opt:
			self.opt = opt
	def clone(self, uri, project = None):
		if project :
			self.cmd.append('clone '+ uri +' '+ project)
		else:
			self.cmd.append('clone '+ uri)
		return(self)
	def clean(self, param=''):
		#git clean -df
		self.cmd.append('clean '+param)
		return(self)
	def init(self):
		if self.workspace :
			self.cmd.append('init')
		return(self)
	def add(self, path, param=''):
		self.cmd.append('add '+path+' '+param)
		return(self)
	def commit(self, msg = '', param=''):
		self.cmd.append('commit '+param+' -m "'+msg+'"')
		return(self)
	def status(self):
		self.cmd.append('status')
		return(self)
	def log(self):
		self.cmd.append('log')
		return(self)
	def pull(self):
		if self.workspace :
			os.chdir(self.workspace)
		self.cmd.append('pull --progress')
		return(self)
	def push(self):
		self.cmd.append('push --progress')
		return(self)
	def reset(self):
		self.cmd.append('reset HEAD --hard')
		return(self)
	def branch(self, branchname=None, op=None):
		os.chdir(self.workspace)
		if branchname :
			if op == 'delete':
				self.cmd.append('branch -D '+branchname)
			elif op == 'new':
				self.cmd.append('checkout -fb '+branchname+' --')
			else:
				self.cmd.append('reset HEAD --hard')
				self.cmd.append('fetch origin')
				self.cmd.append('checkout -f '+branchname)
		else:
			self.cmd.append('branch')
		return(self)
	def merge(self, branchname):
		self.cmd.append('merge '+branchname)
		return(self)
	def tag(self, tagname):
		os.chdir(self.workspace)
		self.cmd.append('tag ' + tagname)
		return(self)
	def checkout(self, revision=None):
		os.chdir(self.workspace)
		if revision :
			self.cmd.append('checkout -f '+revision)
		return(self)
	def debug(self):
		cmd = ''
		for line in self.cmd:
			cmd = 'git ' + line
			self.logger.debug(cmd)
		return(cmd)
	def execute(self):
		for line in self.cmd:
			rev = os.system('git '+ line)
			self.logger.debug('git '+ line)
			self.logger.debug(rev)
			if rev == 256 :
				exit(0)
		self.cmd = []
		print("-")

class GitBranch(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def show(self):
		self.cmd.append('branch --show-current')
	def list(self, pattern = None):
		if pattern :
			self.cmd.append("branch --list '%s'" % pattern)
		else:
			self.cmd.append('branch -l')
	def create(self, name, origin = None):
		if origin :
			self.cmd.append('checkout -b %s origin/%s' % (name, origin))	
		else:
			self.cmd.append('branch %s ' % name)
	def delete(self, name):	
		self.cmd.append('branch --delete %s ' % name)
	def move(self, old, new):
		self.cmd.append('checkout %s' % old)
		self.cmd.append('branch -m "%s" "%s"' % (old, new))
		self.cmd.append('push --delete origin %s' % old)
		self.cmd.append('push origin %s' % new)
		pass

class GitMerge(Git):
	def __init__(self,workspace = None, logger = None):
		super().__init__(workspace, logger)
	def source(self, name):
		self.src = name
		self.cmd.append('fetch origin')
		self.cmd.append('checkout "%s"' % name)
		self.cmd.append('branch --show-current')
		return(self)
	def target(self, name):
		self.tgt = name
		self.cmd.append('fetch origin')
		self.cmd.append('checkout "%s"' % name)
		self.cmd.append('branch --show-current')
		return(self)
	def merge(self):
		self.cmd.append('merge --no-ff  "%s"' % self.src)
		return(self)
	def push(self):
		self.cmd.append('push --set-upstream origin %s' % self.tgt)
		# self.cmd.append('push origin')
		return(self)

class GitUtility(Git):
	def __init__():
		pass