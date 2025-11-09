# Эта переменная в env'ах нужна для docker-compose: локальные пути будут определяться корректно
export PWD := $(shell pwd)

hello:
	@echo 'Hello!'
