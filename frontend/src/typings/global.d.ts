declare global {
  interface WorkingTime {
    id: string
    description: string
    start_time: string
    end_time: string
    worked_time: string
    marked: boolean
  }

  interface WorkingDate {
    date: string
    total_worked_time: string
    working_times: WorkingTime[]
  }
}

export {}
