#!/usr/bin/env ruby
# Encoding: utf-8

require 'open3'
require 'yaml'
require 'uri'
# require 'tqdm'

def get_stud_info
  if File.exist?('repos.yml')
    YAML.load_file('repos.yml')
  elsif File.exist?('.git')
    { '.' => [{
        'url' => '.',
        'path' => '.',
        'branch' => `git branch --show-current`.strip  # git branch --show-current
    }]}
  end
end

def o3c3 *ca, **kw
  o, e, c = Open3::capture3 *ca
  if c.exitstatus != 0
    if kw[:verbose]
      STDERR.puts "#{ca.join(' ')} ended with error: #{e}"
    end
    if kw[:verbose].kind_of?(Integer) && kw[:verbose] > 1
      puts "Output: #{o}"
    end
    false
  else
    true
  end
end

def iter_repos
  get_stud_info.each do | s, rr |  # get_stud_info.tqdm.each
    puts "Студент: #{s}"
    if rr.size == 0
      puts " - !! не опубликовал репозиториев..."
    else
      Dir.mkdir(s) unless File.exist?(s)
      Dir.chdir s do
        rr.each do | r |
          url = r['url']
          path = if r['path']
            r['path']  # любители назвать репозиторий "-."
          else
            URI(url).path.split('/').last.sub(".git", "")  # обычные люди
          end
          branch = r.fetch('branch', 'main')
          yield url, path, branch
        end
      end
    end
  end
end

def init_repo r, rpa, br
  puts " - клонируем <#{r}> -> <#{rpa}>..."
  if o3c3 'git', 'clone', '--', r, rpa
    Dir::chdir rpa do
      o3c3 'git', 'config', 'core.autocrlf', 'input'
      o3c3 'git', 'branch', '-a'
      o3c3 'git', 'switch', br
    end
  end
end

def rcu_repo r, rpa, br
  puts " - обновляем <#{r}> ..."
  Dir::chdir rpa do
    o3c3 'git', 'clean', '-fdX'
    o3c3 'git', 'restore', '.'
    o3c3 'git', 'switch', br
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
