import { useEffect, useState, useRef } from 'react'
import axios from 'axios'

export default function WorkingClock() {
  const inputRef = useRef<HTMLInputElement>(null)
  const [date, setDate] = useState('')
  // const [totalWorkedTime, setTotalWorkedTime] = useState('')
  // const [workingTimes, setWorkingTimes] = useState<WorkingTime[]>([])

  const handleClick = () => {
    inputRef.current && setDate(inputRef.current.value)
  }

  const fetchWorkingTime = (date: string) => {
    axios.get<WorkingDate>('http://127.0.0.1:8000/api/working-time', {
      params: { date }
    })
      .then(({ data }) => console.log(data))
      .catch(error => console.log(error))
  }

  useEffect(() => {
    const dt = new Date()

    const year = dt.getFullYear()
    const month = (dt.getMonth() + 1).toString().padStart(2, '0')
    const day = dt.getDate().toString().padStart(2, '0')

    setDate(`${year}-${month}-${day}`)
  }, [])

  useEffect(() => {
    if (!date) {
      return
    } 

    if (inputRef.current) {
      inputRef.current.value = date
    }

    fetchWorkingTime(date)
  }, [date])

  return (
    <>
      <h1>Hello World</h1>
      <input type="date" ref={inputRef} />
      <button onClick={handleClick}>Filtrar</button>
    </>
  )
}
