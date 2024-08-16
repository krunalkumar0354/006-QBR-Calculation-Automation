from datetime import datetime

def unix_timestamp_to_datetime(timestamp_str):
    return datetime.utcfromtimestamp(int(timestamp_str) / 1000)

def QBR_Table(curr_month):
  table = [
    [[1,2,3],[4,5,6],[7,8,9],[10,11,12]],
    [[2,3,4],[5,6,7],[8,9,10],[11,12,1]],
    [[3,4,5],[6,7,8],[9,10,11],[12,1,2]],
    [[4,5,6],[7,8,9],[10,11,12],[1,2,3]],
    [[5,6,7],[8,9,10],[11,12,1],[2,3,4]],
    [[6,7,8],[9,10,11],[12,1,2],[3,4,5]],
    [[7,8,9],[10,11,12],[1,2,3],[4,5,6]],
    [[8,9,10],[11,12,1],[2,3,4],[5,6,7]],
    [[9,10,11],[12,1,2],[3,4,5],[6,7,8]],
    [[10,11,12],[1,2,3],[4,5,6],[7,8,9]],
    [[11,12,1],[2,3,4],[5,6,7],[8,9,10]],
    [[12,1,2],[3,4,5],[6,7,8],[9,10,11]]
  ]
  return table[curr_month-1]

def main(event):
  # Use inputs to get data from any action in your workflow and use it in your code instead of having to use the HubSpot API.
  act_date = event.get('inputFields').get('activation_date')
  activation_date = unix_timestamp_to_datetime(act_date)
  act_day, act_month, act_year = activation_date.day, activation_date.month, activation_date.year
  current_date = datetime.now()
  curr_day, curr_month, curr_year = current_date.day, current_date.month, current_date.year
  applicable_column = QBR_Table(act_month)
  prep_month, sched_month, qbr_month = 0,0,0
  qbr_day, qbr_year = 1, curr_year
  current_quarter = []
  next_quarter = []
  for i in range(0,len(applicable_column)):
    if curr_month in applicable_column[i]:
      current_quarter = applicable_column[i]
      if i == 3:
        #year change happening.
        next_quarter = applicable_column[0]
        print(next_quarter)
        qbr_year += 1
        break
      else:
        next_quarter = applicable_column[i+1]
  
  counter = 0
  
  for i in current_quarter:
    if curr_year + 1 == qbr_year:
      #year change happening
      prep_month = next_quarter[0]
      sched_month = next_quarter[1]
      qbr_month = next_quarter[2]
      break
    if curr_month == i:
      prep_year, sched_year, qbr_year = curr_year, curr_year, curr_year
      if counter == 0:
        prep_month, sched_month, qbr_month = current_quarter[counter], current_quarter[counter + 1], current_quarter[counter + 2]
        break
      if counter == 1:
        prep_month, sched_month, qbr_month = current_quarter[counter - 1], current_quarter[counter], current_quarter[counter + 1]
        break
      if counter == 2:
        #quarter change happening.
        prep_month, sched_month, qbr_month = next_quarter[0], next_quarter[1], next_quarter[2]
        break
    else:
      counter += 1
  prep_day, sched_day, qbr_day = act_day, act_day, act_day
  if prep_month == 12:
    prep_year, sched_year, qbr_year = curr_year, curr_year + 1, curr_year + 1
  elif sched_month == 12:
    prep_year, sched_year, qbr_year = curr_year, curr_year, curr_year + 1
  elif curr_month == 12:
    prep_year, sched_year, qbr_year = curr_year + 1, curr_year + 1, curr_year + 1
  else :
    prep_year, sched_year, qbr_year = curr_year, curr_year, curr_year
  preparation_date = str(prep_day) + "-" + str(prep_month) + "-" + str(prep_year)
  scheduling_date = str(sched_day) + "-" + str(sched_month) + "-" + str(sched_year)
  QBR_date = str(qbr_day) + "-" + str(qbr_month) + "-" + str(qbr_year)
  # Return the output data that can be used in later actions in your workflow.
  preparation_date = datetime.strptime(preparation_date, '%d-%m-%Y')
  scheduling_date = datetime.strptime(scheduling_date, '%d-%m-%Y')
  QBR_date = datetime.strptime(QBR_date, '%d-%m-%Y')
  preparation_date = int(preparation_date.timestamp()*1000)
  scheduling_date = int(scheduling_date.timestamp()*1000)
  QBR_date = int(QBR_date.timestamp()*1000)
  return {
    "outputFields": {
      "Activation_Date": act_date,
      "Preparation_Date": preparation_date,
      "Scheduling_Date": scheduling_date,
      "QBR_Date": QBR_date
    }
  }