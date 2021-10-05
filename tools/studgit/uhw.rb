#!/usr/bin/env ruby
# Encoding: utf-8

require 'open3'
require 'yaml'
require 'uri'
require 'tqdm'

def get_stud_info
  YAML.load_file('repos.yml')
end

def o3c3(*ca)
  o, e, c = Open3::capture3 *ca
  if c.exitstatus != 0
    STDERR.puts "#{ca.join(' ')} ended with error: #{e}"
    puts "Output: #{o}"
    false
  else
    true
  end
end

def iter_repos
  get_stud_info.tqdm.each do | s, rr |
    puts "Студент: #{s}"
    if rr.size == 0
      puts " - !! не опубликовал репозиториев..."
    else
      Dir.mkdir(s) unless File.exist?(s)
      Dir.chdir s do
        rr.each do | r |
          u, d = if !r.kind_of?(Array) # Обычные люди
            [r, URI(r).path.split('/').last.sub(".git", "")]
          else # любители назвать репозиторий "-."
            r # r[0], r[1]
          end
          yield u, d
        end
      end
    end
  end
end

def init_repo r, rpa
  puts " - клонируем <#{r}> -> <#{rpa}>..."
  if o3c3 'git', 'clone', '--', r, rpa
    Dir::chdir rpa do
      o3c3 'git', 'config', 'core.autocrlf', 'input'
    end
  end
end

def rcu_repo r, rpa
  puts " - обновляем <#{r}> ..."
  Dir::chdir rpa do
    o3c3 'git', 'clean', '-fdX'
    o3c3 'git', 'restore', '.'
    o3c3 'git', 'pull', '--all', '--tags', '--rebase'
  end
end

# p ARGV

case ARGV[0]
when 'i'
  iter_repos &method(:init_repo)
when 'u'
  iter_repos &method(:rcu_repo)
end
