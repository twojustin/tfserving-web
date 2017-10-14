class PagesController < ApplicationController

  def index
    response = `cat /etc/hosts`
    render plain: response, status: :ok
  end
end
