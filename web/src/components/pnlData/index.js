import React, { useEffect, useState, useRef } from 'react'
import { Table } from 'react-bootstrap'
import dateFormat from 'dateformat'
import { motion } from 'framer-motion'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

export const PnlData = () => {
  const [tableData, setTableData] = useState([])
  const bottomRef = useRef(null)
  const channel = dateFormat(new Date(), 'yyyymmdd')
  const socket = '127.0.0.1:3001'
  const ws = useRef(new WebSocket(`ws://${socket}/ws/sub/${channel}`)).current
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    const handleOpen = () => {
      setIsConnected(true)
      toast.success('Connection to the server established successfully!')
    }

    const handleMessage = (e) => {
      const data = JSON.parse(JSON.parse(e.data))
      setTableData((prevData) => [
        ...prevData,
        { key: data.ssid, data: data.timestamp },
      ])
    }

    const handleError = () => {
      toast.error("Can't establish connection to the server!")
      setIsConnected(false)
    }

    const handleClose = () => {
      if (isConnected) {
        toast.warn('Connection to the server has been terminated!')
        setIsConnected(false)
      }
    }

    ws.addEventListener('open', handleOpen)
    ws.addEventListener('message', handleMessage)
    ws.addEventListener('error', handleError)
    ws.addEventListener('close', handleClose)

    return () => {
      ws.removeEventListener('open', handleOpen)
      ws.removeEventListener('message', handleMessage)
      ws.removeEventListener('error', handleError)
      ws.removeEventListener('close', handleClose)
      ws.close()
    }
  }, [])

  const scrollToBottom = () => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [tableData])

  return (
    <div>
      <Table striped bordered hover>
        <thead style={{ position: 'sticky', top: '0' }}>
          <tr>
            <th>N.</th>
            <th>SSID</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, index) => {
            return (
              <motion.tr
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                layout
                key={row.key}
                transition={{
                  opacity: { duration: 0.5 },
                }}
              >
                <td>{index + 1}</td>
                <td>{row.key}</td>
                <motion.td
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  layout
                  key={row.key}
                  transition={{
                    opacity: { duration: 0.5 },
                  }}
                >
                  {row.data}
                </motion.td>
              </motion.tr>
            )
          })}
        </tbody>
      </Table>
      <ToastContainer />
      <div ref={bottomRef} />
    </div>
  )
}
